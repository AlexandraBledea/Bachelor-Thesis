from abc import ABC
import os
from data_processing.command import Command


class EmoDataset(Command, ABC):

    def __init__(self, key, description):
        super().__init__(key, description)
        self.__paths = []
        self.__labels = []
        self.__file_path = super().path + 'emo'

    def execute(self):
        for dirname, _, filenames in os.walk('wav'):
            for filename in filenames:
                self.__paths.append(os.path.join(dirname, filename))

                label = list(filename)

                if label[5] == 'F':
                    self.__labels.append("happiness")
                elif label[5] == 'W':
                    self.__labels.append("anger")
                elif label[5] == 'L':
                    self.__labels.append("boredom")
                elif label[5] == 'E':
                    self.__labels.append("disgust")
                elif label[5] == 'A':
                    self.__labels.append("fear")
                elif label[5] == 'T':
                    self.__labels.append("sadness")
                elif label[5] == 'N':
                    self.__labels.append("neutral")

        print('EMO German Dataset is loaded')
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