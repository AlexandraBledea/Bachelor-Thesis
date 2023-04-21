from abc import ABC
from data_processing.command import Command

import os


class RavdessDataset(Command, ABC):

    def __init__(self, key, description):
        super().__init__(key, description)
        self.__paths = []
        self.__labels = []
        self.__intensity = []
        self.__file_path = super().path + 'ravdess'

    def execute(self):
        for dirname, _, filenames in os.walk("test_data"):
            for filename in filenames:
                self.__paths.append(os.path.join(dirname, filename))

                label = filename.split('-')
                emotion_label = label[2]
                intensity_label = label[3]

                if emotion_label == "03":
                    self.__labels.append("happiness")
                elif emotion_label == "05":
                    self.__labels.append("anger")
                elif emotion_label == "07":
                    self.__labels.append("disgust")
                elif emotion_label == "06":
                    self.__labels.append("fear")
                elif emotion_label == "04":
                    self.__labels.append("sadness")
                elif emotion_label == "01":
                    self.__labels.append("neutral")
                elif emotion_label == "02":
                    self.__labels.append("calm")
                elif emotion_label == "08":
                    self.__labels.append("surprised")

                if intensity_label == "01":
                    self.__intensity.append("normal")
                elif intensity_label == "02":
                    self.__intensity.append("strong")

        print('RAVDESS Dataset is loaded')
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
