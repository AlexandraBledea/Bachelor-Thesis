from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def execute(self, recording, actual_label):
        pass