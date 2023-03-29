from abc import ABC
import os
from src.data_processing.command import Command


class TessDataset(Command, ABC):

    def __init__(self, key, description):
        super().__init__(key, description)
        self.__paths = []
        self.__labels = []
        self.__file_path = super().path + 'tess'

    def execute(self):
        print(self.__file_path)
        for dirname, _, filenames in os.walk(self.__file_path):
            for filename in filenames:
                self.__paths.append(os.path.join(dirname, filename))
                label = filename.split('_')[-1]
                label = label.split('.')[0]

                if label == "angry":
                    self.__labels.append("anger")
                elif label == "disgust":
                    self.__labels.append("disgust")
                elif label == "fear":
                    self.__labels.append("fear")
                elif label == "happy":
                    self.__labels.append("happiness")
                elif label == "neutral":
                    self.__labels.append("neutral")
                elif self.__labels == "ps":
                    self.__labels.append("surprised")

                self.__labels.append(label.lower())

        print('TESS Toronto Dataset is loaded')
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
