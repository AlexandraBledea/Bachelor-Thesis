from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def execute(self, recording, actual_label):
        pass

    @abstractmethod
    def get_strategy_name(self):
        pass
