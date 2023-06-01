import pandas as pd
from repository.repository import Repository
from database import User, Recording
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import os
from datetime import datetime, timedelta
from flask_jwt_extended import  create_access_token
from models.Strategy import Strategy

from models.EnglishTessModel import EnglishTessModel
from models.EnglishRavdessModel import EnglishRavdessModel
from models.EnglishRavdessModel2 import EnglishRavdessModel2

from models.EnglishModel import FirstModel
class Service:

    strategy: Strategy

    def __init__(self, database):
        self.__repository = Repository(database)
        self.__strategies = {}
        self.__initialize_models()

    def __initialize_models(self):
        self.__strategies['English Tess'] = EnglishRavdessModel2()
        self.__strategies['English Ravdess'] = EnglishRavdessModel()

    def predict_emotion(self, strategy_name, audio, actual_emotion):
        return self.__strategies[strategy_name].execute(audio, actual_emotion)

    def add_recording(self, actualEmotion, audio, model, email, predicted_emotion, statistics):

        new_recording = Recording(actualEmotion, predicted_emotion, bytes(audio), model, email,
                                  str(statistics))


        self.__repository.add_recording(new_recording)

        return new_recording

    def find_best_model(self, audio, actual_emotion):

        final_predictions = []
        final_percentages = []
        final_statistics = []
        strategy_name = []

        for strategy in self.__strategies.values():
            prediction, statistics = strategy.execute(audio, actual_emotion)

            strategy_name.append(strategy.get_strategy_name())
            final_predictions.append(prediction)
            final_percentages.append(statistics[actual_emotion])
            final_statistics.append(statistics)

        index = final_percentages.index(max(final_percentages))
        model_name = strategy_name[index]

        return model_name, final_predictions[index], final_statistics[index]


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

