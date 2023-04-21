class Repository:

    def __init__(self):
        self.__paths = []
        self.__labels = []
        self.__intensity = []

    def add_paths(self, values):
        self.__paths = self.__paths + values

    def add_labels(self, values):
        self.__labels = self.__labels + values

    def add_intensities(self, values):
        self.__intensity = self.__intensity + values

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
