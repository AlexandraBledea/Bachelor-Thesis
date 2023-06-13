from database import User


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
