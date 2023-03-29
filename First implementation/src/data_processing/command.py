from abc import ABC, abstractmethod
from jproperties import Properties


"""
Declare an abstract class for executing an operation.
"""


class Command(ABC):

    def __init__(self, key, description):
        self.__key = key
        self.__description = description
        self._file_path = self.__initialize_properties()

    def __initialize_properties(self):
        configs = Properties()
        with open('settings.properties', 'rb') as read_properties:
            configs.load(read_properties)

        return configs['path'].data

    @property
    def path(self):
        return self._file_path;

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @abstractmethod
    def execute(self):
        pass
