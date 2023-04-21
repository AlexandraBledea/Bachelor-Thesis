import pandas as pd
from data_processing.language_based.english.tess_dataset import TessDataset
from data_processing.language_based.english.savee_dataset import SaveeDataset
from data_processing.language_based.english.ravdess_dataset import RavdessDataset
from data_processing.language_based.english.cremad_dataset import CremaDDataset
from data_processing.language_based.german.emo_dataset import EmoDataset


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

    def initialize_german_database(self, dataset):
        if dataset == "emo":
            emo_db = EmoDataset("emo", "german")
            self.init_emo(emo_db)

    def initialize_english_database(self, dataset):

        if dataset == "tess":
            tess_db = TessDataset("tess", "english")
            self.init_tess(tess_db)

        elif dataset == "ravdess":
            ravdess_db = RavdessDataset("ravdess", "english")
            self.init_ravdess(ravdess_db)

        elif dataset == "savee":
            savee_db = SaveeDataset("savee", "english")
            self.init_savee(savee_db)

        elif dataset == "cremad":
            cremad_db = CremaDDataset("cremad", "english")
            self.init_cremad(cremad_db)

        elif dataset == "all":
            tess_db = TessDataset("tess", "english")
            ravdess_db = RavdessDataset("ravdess", "english")
            savee_db = SaveeDataset("savee", "english")
            cremad_db = CremaDDataset("cremad", "english")

            self.init_tess(tess_db)
            self.init_ravdess(ravdess_db)
            self.init_savee(savee_db)
            self.init_cremad(cremad_db)


    def init_emo(self, emo_db):
        paths, labels = emo_db.execute()
        self.initialize_repository(paths, labels)
    def init_savee(self, savee_db):
        paths, labels = savee_db.execute()
        self.initialize_repository(paths, labels)

    def init_ravdess(self, ravdess_db):
        paths, labels = ravdess_db.execute()
        self.initialize_repository(paths, labels)

    def init_tess(self, tess_db):
        paths, labels = tess_db.execute()
        self.initialize_repository(paths, labels)

    def init_cremad(self, cremad_db):
        paths, labels = cremad_db.execute()
        self.initialize_repository(paths, labels)

    def paths(self):
        return self.__repository.paths

    def labels(self):
        return self.__repository.labels

    # def plot_data(self):

