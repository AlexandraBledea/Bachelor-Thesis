import os
from abc import ABC

from src.data_processing.command import Command


class SaveeDataset(Command, ABC):

    def __init__(self, key, description):
        super().__init__(key, description)
        self.__paths = []
        self.__labels = []
        self.__file_path = super().path + 'savee'

    def execute(self):
        print(self.__file_path)
        for dirname, _, filenames in os.walk(self.__file_path):
            for filename in filenames:
                self.__paths.append(os.path.join(dirname, filename))
                label = filename.split('.')[0]
                label = list(label)

                if label[0] == 'a':
                    self.__labels.append("anger")
                elif label[0] == 'd':
                    self.__labels.append("disgust")
                elif label[0] == 'f':
                    self.__labels.append("fear")
                elif label[0] == "h":
                    self.__labels.append("happiness")
                elif label[0] == "n":
                    self.__labels.append("neutral")
                elif label[0] == "s" and label[1] == "a":
                    self.__labels.append("sadness")
                elif label[0] == "s" and label[1] == "u":
                    self.__labels.append("surprised")

        print('Savee Dataset is loaded')
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
