from src.repository.repository import Repository
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import librosa
import librosa.display
from IPython.display import Audio
import warnings
import tensorflow as tf
from sklearn.model_selection import train_test_split
class Service:

    def __init__(self, repo):
        self.__repository = repo
        self.__data_frame = pd.DataFrame()

    def initialize_repository(self, paths, labels):
        self.add_paths_and_labels(paths, labels)

    def add_paths_and_labels(self, paths, labels):
        self.__repository.add_paths(paths)
        self.__repository.add_labels(labels)

    def create_data_frame(self):
        self.__data_frame['speech'] = self.__repository.paths
        self.__data_frame['label'] = self.__repository.add_labels

    def plot_data(self):

