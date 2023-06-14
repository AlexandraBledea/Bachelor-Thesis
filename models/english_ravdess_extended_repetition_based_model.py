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


class EnglishRavdessExtendedRepetitionBasedModel(Strategy, ABC):

    def __init__(self):

        self.__path = "https://github.com/AlexandraBledea/Bachelor-Thesis-Backend/blob/00c5c8f2b76cef58849f762eb7b215f7f1264b21/in-memory-models/english-ravdess-extended-repetition-based/"
        self.__model = load_model(self.__path + "training_model_experiment_x.h5")
        self.__encoder = self.__load_one_hot_encoder()
        self.__scaler = self.__load_standard_scaler()

    def __load_one_hot_encoder(self):
        features_ravdess = pd.read_csv(self.__path + 'features_ravdess.csv')
        features_alexandra_train = pd.read_csv(self.__path + 'features_alexandra_train.csv')
        features_alexandra_test = pd.read_csv(self.__path + 'features_alexandra_test.csv')
        features_alexandra_validation = pd.read_csv(self.__path + 'features_alexandra_validation.csv')

        Y_ravdess = features_ravdess['labels'].values
        Y_alexandra_train = features_alexandra_train['labels'].values
        Y_alexandra_test = features_alexandra_test['labels'].values
        Y_alexandra_validation = features_alexandra_validation['labels'].values

        labels = np.concatenate((Y_ravdess, Y_alexandra_train, Y_alexandra_test, Y_alexandra_validation), axis=0)
        enc = OneHotEncoder()
        enc.fit_transform(labels.reshape(-1, 1))

        return enc

    def __load_standard_scaler(self):
        scaler = joblib.load(self.__path + 'scaler.pk1')
        return scaler

    def execute(self, recording):
        byte_array = bytes(recording)
        self.__save_and_load_temporary_file(byte_array)
        prediction, statistics = self.__predict_emotion()
        self.__delete_file()
        return prediction, statistics

    def __delete_file(self):
        file_path = self.__path + 'temp.wav'
        os.remove(file_path)

    def get_strategy_name(self):
        return "Ravdess Extended Repetition Based"

    def __save_and_load_temporary_file(self, byte_array):
        with open(self.__path + 'temp.wav', mode='wb') as f:
            f.write(byte_array)

    def __load_temporary_file(self):
        signal, sample_rate = librosa.load(self.__path + 'temp.wav')
        return signal, sample_rate

    def __get_features(self):
        signal, sample_rate = self.__load_temporary_file()
        result = DataProcessing.extract_mel_spect_features(signal, sample_rate)
        result = np.array(result)

        return result

    def __process_features(self):
        x_predict = self.__get_features()
        x_predict = np.expand_dims(x_predict, axis=1)
        x_predict = np.transpose(x_predict)
        x_predict = self.__scaler.transform(x_predict)
        x_predict = np.expand_dims(x_predict, axis=1)
        return x_predict

    def __predict_emotion(self):
        x_predict = self.__process_features()

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
