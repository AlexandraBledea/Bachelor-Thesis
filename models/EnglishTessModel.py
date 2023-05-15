import io
from abc import ABC

import librosa
import numpy as np
import pandas as pd
from keras.models import load_model
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
import joblib

from features.FeaturesExtraction import FeaturesExtraction
from models.Strategy import Strategy


class EnglishTessModel(Strategy, ABC):

    def __init__(self):
        self.__path = "C:\\Users\\night\\Desktop\\Facultate An 3\\Thesis\\EXPERIMENTS\\Model 41 - TESS - Data Augmentation - No Dropouts - Attention Based - adam optimizer\\"
        self.__model = load_model(self.__path + "training_model_experiment_x.h5")
        self.__encoder = self.__load_one_hot_encoder()
        self.__scaler = self.__load_standard_scaler()

    def __load_one_hot_encoder(self):
        features = pd.read_csv(self.__path + 'features.csv')
        Y = features['labels'].values
        enc = OneHotEncoder()
        enc.fit_transform(Y.reshape(-1, 1))

        return enc

    def __load_standard_scaler(self):
        scaler = joblib.load(self.__path + 'scaler.pk1')
        return scaler

    def execute(self, recording, actual_label):
        byte_array = bytes(recording)

        self.__save_and_load_temporary_file(byte_array)
        return self.__predict_emotion(actual_label)

    def __save_and_load_temporary_file(self, byte_array):
        with open(self.__path + 'temp.wav', mode='wb') as f:
            f.write(byte_array)

    def __load_temporary_file(self):
        signal, sample_rate = librosa.load(self.__path + 'temp.wav')
        return signal, sample_rate

    def __get_features(self):
        signal, sample_rate = self.__load_temporary_file()

        result = FeaturesExtraction.extract_features(signal, sample_rate)
        result = np.array(result)

        return result

    def __process_features(self, actual_label):
        x_predict = self.__get_features()
        y_predict = actual_label

        predicts = pd.DataFrame(x_predict)
        predicts['labels'] = y_predict
        x_predict = predicts.iloc[:, :-1].values
        x_predict = np.array(x_predict)
        x_predict = np.transpose(x_predict)
        x_predict = self.__scaler.transform(x_predict)
        x_predict = np.expand_dims(x_predict, axis=2)

        return x_predict

    def __predict_emotion(self, actual_label):
        x_predict = self.__process_features(actual_label)

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

        labels = self.__decode_labels(prediction)

        percentages = [val * 100 for val in prediction[0]]

        return prediction_label, percentages, labels

    def __decode_labels(self, prediction):
        labels = []

        for index in range(0, len(prediction[0])):
            prediction_index_2d = np.zeros_like(prediction)
            prediction_index_2d[0][index] = 1
            prediction_label_enc = self.__encoder.inverse_transform(prediction_index_2d)
            prediction_label = prediction_label_enc[0][0]

            labels.append(prediction_label)

        return labels

