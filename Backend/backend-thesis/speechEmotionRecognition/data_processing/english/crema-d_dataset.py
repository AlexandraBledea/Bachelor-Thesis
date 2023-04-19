from abc import ABC
import os
from speechEmotionRecognition.data_processing.command import Command


class CremaDDataset(Command, ABC):

    def __init__(self, key, description):
        super().__init__(key, description)
        self.__paths = []
        self.__labels = []
        self.__intensity = []
        self.__file_path = super().path + 'crema-d'

    def execute(self):
        for dirname, _, filenames in os.walk("CREMA-D"):
            for filename in filenames:
                self.__paths.append(os.path.join(dirname, filename))

                label = filename.split('_')

                if label[2] == "HAP":
                    self.__labels.append("happiness")
                elif label[2] == "ANG":
                    self.__labels.append("anger")
                elif label[2] == "DIS":
                    self.__labels.append("disgust")
                elif label[2] == "FEA":
                    self.__labels.append("fear")
                elif label[2] == "SAD":
                    self.__labels.append("sadness")
                elif label[2] == "NEU":
                    self.__labels.append("neutral")

                intensity_label = label[3].split('.')

                if intensity_label[0] == "MD":
                    self.__intensity.append("medium")
                elif intensity_label[0] == "LO":
                    self.__intensity.append("low")
                elif intensity_label[0] == "HI":
                    self.__intensity.append("high")
                elif intensity_label[0] == "XX":
                    self.__intensity.append("unspecified")

        print('CREMA-D  Dataset is loaded')
        return self.__paths, self.__labels


    @property
    def paths(self):
        return self.__paths

    @paths.setter
    def paths(self, values):
        self.__paths = values

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, values):
        self.__labels = values

    @property
    def intensity(self):
        return self.__intensity

    @intensity.setter
    def intensity(self, values):
        self.__intensity = values

