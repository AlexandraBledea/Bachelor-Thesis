import pandas as pd
from repository.repository import Repository
from database import User, Recording
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import os
from datetime import datetime, timedelta
from flask_jwt_extended import  create_access_token
from models.Strategy import Strategy

from models.EnglishModel import FirstModel
class Service:

    strategy: Strategy
    def __init__(self, database):
        self.__repository = Repository(database)

    def set_strategy(self, strategy: Strategy):
        self.__strategy = strategy

    def predict_emotion(self, audio, actual_emotion):
        return self.__strategy.execute(audio, actual_emotion)

    def add_recording(self, data, predicted_emotion, percentages, labels):
        print(percentages)
        print(labels)

        new_recording = Recording(data['actualEmotion'], predicted_emotion, bytes(data['audio']), data['model'], data['userEmail'],
                                  labels, percentages)

        print(new_recording.statistics_percentages)
        print(new_recording.statistics_labels)

        self.__repository.add_recording(new_recording)

        return new_recording

    # def find_best_model(self, strategy1, strategy2):



    def register_user(self, data):
        user = self.__repository.find_user_by_email(data['email'])

        if user is None:
            hashed_pw = generate_password_hash(data['password'], "sha256", salt_length=8)

            new_user = User(data['firstname'], data['lastname'], data['gender'], data['email'].lower(), hashed_pw)
            self.__repository.add_user(new_user)

            response = {'Message': 'Account created successfully!'}
            return response

        else:

            response = {'Message': 'There exists an account with the given email!'}
            return response

    def change_password(self, data):

        user = self.__repository.find_user_by_email(data['email'])

        if user is not None:
            if check_password_hash(user.password, data['oldPassword']):
                hashed_pw = generate_password_hash(data['newPassword'], "sha256", salt_length=8)

                self.__repository.change_password(user, hashed_pw)

                response = {'Message': 'Password changed successfully!'}

                return response

            else:
                response = {'Message': 'Invalid password or email'}
                return response

        else:
            response = {'Message': 'Invalid password or email'}
            return response

    def login(self, data):

        data['email'] = data['email'].lower()

        user = self.__repository.find_user_by_email(data['email'])

        if user is not None:
            if check_password_hash(user.password, data['password']):

                token = create_access_token(
                    identity=data['email'])

                # token = jwt.encode({
                #     'email': data['email'],
                #     'expiration': str(datetime.utcnow() + timedelta(minutes=30))
                # },
                #     os.getenv("SECRET_KEY"),
                #     algorithm='HS256')

                self.__repository.initialize_recordings(data['email'])

                response = {'token': token}
                return response


        return {'token': ''}

    def get_recordings(self):
        return self.__repository.get_recordings()

    def get_recordings_for_user(self, data):

        user = self.__repository.find_user_by_email(data)

        if user is not None:

            return user.json()['recordings']


        else:

            return {'Message': 'No user with the given email address'}

