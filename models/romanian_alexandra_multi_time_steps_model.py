import os
from abc import ABC
import librosa
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
import joblib
from features.DataProcessing import DataProcessing
from models.Strategy import Strategy


class RomanianAlexandraMultiTimeStepsModel(Strategy, ABC):

    def __init__(self):
        self.__path = "in-memory-models/romanian-alexandra-multi-time-steps/"
        self.__model = load_model(self.__path + "training_model_experiment_x.h5")
        self.__encoder = self.__load_one_hot_encoder()
        self.__scaler = self.__load_standard_scaler()

    def __load_one_hot_encoder(self):
        features = pd.read_csv(self.__path + 'labels.csv')
        Y = features.values
        enc = OneHotEncoder()
        enc.fit_transform(Y.reshape(-1, 1))
        return enc

    def __load_standard_scaler(self):
        scaler = joblib.load(self.__path + 'scaler.pk1')
        return scaler

    def execute(self, recording):
        byte_array = bytes(recording)
        self.__save_and_load_temporary_file(byte_array)
        signal, sample_rate = self.__load_temporary_file()
        signal = self.preprocess(signal)
        prediction, statistics = self.__predict_emotion(signal, sample_rate)
        self.__delete_file()
        return prediction, statistics

    def __delete_file(self):
        file_path = self.__path + 'temp.wav'
        os.remove(file_path)

    def get_strategy_name(self):
        return "Alexandra Multi Time Steps"

    def __save_and_load_temporary_file(self, byte_array):
        with open(self.__path + 'temp.wav', mode='wb') as f:
            f.write(byte_array)

    def __load_temporary_file(self):
        signal, sample_rate = librosa.load(self.__path + 'temp.wav')
        return signal, sample_rate

    def __get_features(self, signal, sample_rate):
        result = DataProcessing.extract_mel_mfcc_multi_time_steps(signal, sample_rate)
        result = np.stack(result)
        return result

    def preprocess(self, recording):
        # signal = DataProcessing.trim_silence(recording, 48000)
        # signal = DataProcessing.normalize_volume(signal)
        signal = DataProcessing.pad_audio_alexandra(recording)

        return signal

    def __process_features(self, signal, sample_rate):
        x_predict = self.__get_features(signal, sample_rate)
        x_predict = np.expand_dims(x_predict, axis=0)
        x_predict_2 = x_predict.reshape((x_predict.shape[0], -1))
        x_predict_2 = self.__scaler.transform(x_predict_2)
        x_predict = x_predict_2.reshape(x_predict.shape)

        return x_predict

    def __predict_emotion(self, signal, sample_rate):
        x_predict = self.__process_features(signal, sample_rate)

        # We take the models prediction
        prediction = self.__model.predict(x_predict)

        # We take the index of the greatest predicted probability
        prediction_index = np.argmax(prediction)

        # We convert the index to a one-hot encoder vector
        prediction_index_2d = np.zeros_like(prediction)
        prediction_index_2d[0][prediction_index] = 1

        # Inverse transform the one-hot encoded vector to get the predicted label
        prediction_label_enc = self.__encoder.inverse_transform(prediction_index_2d)
        prediction_label = prediction_label_enc[0][0]

        labels = DataProcessing.decode_labels(prediction, self.__encoder)
        res = DataProcessing.create_percentages_for_emotions(labels, prediction[0])

        return prediction_label, res
