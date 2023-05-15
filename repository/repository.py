from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash

from database import User, Recording


class Repository:

    def __init__(self, database):
        self.__recordings = []
        self.__db = database

    def find_user_by_email(self, email):
        return self.__db.session.query(User).filter(User.email == email).first()

    def add_user(self, new_user):
        self.__db.session.add(new_user)
        self.__db.session.commit()
        self.__db.session.flush()

    def change_password(self, user, new_hashed_password):
        user.password = new_hashed_password
        self.__db.session.commit()
        self.__db.session.flush()

    def add_recording(self, recording):
        self.__db.session.add(recording)
        self.__db.session.commit()
        self.__db.session.flush()

        self.__recordings.append(recording.json())

    def initialize_recordings(self, email):
        self.__recordings = []
        user = self.find_user_by_email(email)
        self.__recordings = user.json()['recordings']

    def get_recordings(self):
        return self.__recordings

    # def get_recordings_for_user(self, email):
    #     user = (
    #         self.__db.session.query(User)
    #         .options(joinedload(User.recordings))
    #         .filter(User.email == email)
    #         .first()
    #     )
    #
    #     serialized_recordings = [recording.json() for recording in recordings]
    #     print(serialized_recordings)
    #     return serialized_recordings

    # @property
    # def paths(self):
    #     return self.__paths
    #
    # @paths.setter
    # def paths(self, values):
    #     self.__paths = values
    #
    # @property
    # def labels(self):
    #     return self.__labels
    #
    # @labels.setter
    # def labels(self, values):
    #     self.__labels = values
    #
    # @property
    # def intensity(self):
    #     return self.__intensity
    #
    # @intensity.setter
    # def intensity(self, values):
    #     self.__intensity = values
