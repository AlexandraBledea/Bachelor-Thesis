from repository.repository import Repository
from database import User, Recording
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from flask_jwt_extended import create_access_token
from models.Strategy import Strategy
from models.romanian_alexandra_repetition_based_model import RomanianAlexandraRepetitionBasedModel
from models.romanian_alexandra_spectral_axis_model import RomanianAlexandraSpectralAxisModel
from models.english_ravdess_repetition_based_model import EnglishRavdessRepetitionBasedModel
from models.english_ravdess_spectral_axis_model import EnglishRavdessSpectralAxisModel
from models.english_ravdess_extended_repetition_based_model import EnglishRavdessExtendedRepetitionBasedModel
from models.romanian_alexandra_multi_time_steps_model import RomanianAlexandraMultiTimeStepsModel
from models.english_ravdess_multi_time_steps_model import EnglishRavdessMultiTimeStepsModel
from collections import Counter


class Service:
    strategy: Strategy

    def __init__(self, database):
        self.__repository = Repository(database)
        self.__strategies = {}
        self.__initialize_models()

    def __initialize_models(self):
        self.__strategies['Alexandra Repetition Based'] = RomanianAlexandraRepetitionBasedModel()
        self.__strategies['Alexandra Spectral Axis'] = RomanianAlexandraSpectralAxisModel()
        self.__strategies['Ravdess Spectral Axis'] = EnglishRavdessSpectralAxisModel()
        self.__strategies['Ravdess Repetition Based'] = EnglishRavdessRepetitionBasedModel()
        self.__strategies['Ravdess Extended Repetition Based'] = EnglishRavdessExtendedRepetitionBasedModel()
        self.__strategies['Ravdess Multi Time Steps'] = EnglishRavdessMultiTimeStepsModel()
        self.__strategies['Alexandra Multi Time Steps'] = RomanianAlexandraMultiTimeStepsModel()

    def predict_emotion(self, strategy_name, audio):
        return self.__strategies[strategy_name].execute(audio)

    def add_recording(self, actual_emotion, audio, model, email, predicted_emotion, statistics):

        new_recording = Recording(actual_emotion, predicted_emotion, bytes(audio), model, email,
                                  str(statistics))

        self.__repository.add_recording(new_recording)

        return new_recording

    def find_best_prediction(self, audio):

        final_predictions = []

        for strategy in self.__strategies.values():
            prediction, _ = strategy.execute(audio)
            final_predictions.append(prediction)

        # Count the occurrences of each predicted emotion
        emotion_counts = Counter(final_predictions)

        # Get the emotion with the highest count
        majority_emotion = emotion_counts.most_common(1)[0][0]

        return "Collective prediction model", majority_emotion

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
                expiration_time = timedelta(minutes=120)
                token = create_access_token(identity=data['email'], expires_delta=expiration_time)

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
