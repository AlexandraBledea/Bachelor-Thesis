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


class EnglishRavdessModel(Strategy, ABC):

    def __init__(self):
        self.__path = "C:\\Users\\night\\Desktop\\Facultate An 3\\Thesis\\EXPERIMENTS\\RAVDESS EXPERIMENTS V3 - volume normalization\\ATTENTION BASED WITH BATCH NORMALIZATION\\"
        self.__model = load_model(self.__path + "training_model_experiment_x1.h5")
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

        result = FeaturesExtraction.extract_mfcc_features(signal, sample_rate)
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

        plot_bytes = self.__plot_probabilities(prediction[0], labels)

        return prediction_label, plot_bytes

    def __decode_labels(self, prediction):
        labels = []

        for index in range(0, len(prediction[0])):
            prediction_index_2d = np.zeros_like(prediction)
            prediction_index_2d[0][index] = 1
            prediction_label_enc = self.__encoder.inverse_transform(prediction_index_2d)
            prediction_label = prediction_label_enc[0][0]

            labels.append(prediction_label)

        return labels

    def __plot_probabilities(self, probabilities, labels):

        colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']

        # Normalize the values
        # total = sum(probabilities)
        # probabilities = [val / total for val in probabilities]

        # Convert probabilities to percentages
        percentages = [val * 100 for val in probabilities]
        # percentages = [x if x >= 1 else 0 for x in percentages]

        for p in percentages:
            print(p)

        print(sum(percentages))

        # Create the bar plot with percentages
        plt.bar(labels, probabilities)


        print(labels)
        print(probabilities)

        print(sum(probabilities))

        # Set labels and title
        plt.ylabel('Probabilities')
        plt.xlabel('Emotions')
        plt.title('Emotion Probabilities')

        # plt.ylim(0, 100)  #
        # plt.show()
        # # Create explode list with the same length as probabilities
        # explode = [0.3 if p == max(probabilities) else 0.1 for p in probabilities]
        #
        # # plotting the pie chart
        # plt.bar(probabilities, labels=colors, colors=colors,
        #         startangle=90, shadow=True, explode=(0.4, 0.4, 0.4, 0.4, 0.4, 0.4),
        #         radius=1.2, autopct='%1.1f%%')

        # # Set aspect ratio to be equal to have a circular pie chart
        # plt.axis('equal')
        # # Add more colors as needed
        # plt.bar(labels, probabilities, color=colors[:len(labels)])

        # plt.xscale('log')
        # plt.yscale('log')
        # Adjust the y-axis limits to ensure all bars are visible
        # plt.ylim(0, max(probabilities) + max(probabilities) * 0.1)

        # Rotate the x-axis labels if needed
        # plt.xticks(rotation=45)

        # Convert the plot to a byte array

        plt.savefig("temp.png")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        byte_array = buf.getvalue()
        buf.close()

        return byte_array
