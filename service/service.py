import pandas as pd
from repository.repository import Repository
from database import User, Recording
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import os
from datetime import datetime, timedelta
class Service:

    def __init__(self, database):

        self.__repository = Repository(database)


    def register_user(self, data):
        user = self.__repository.find_user_by_email(data['email'])

        if user is None:
            hashed_pw = generate_password_hash(data['password'], "sha256", salt_length=8)

            new_user = User(data['firstname'], data['lastname'], data['gender'], data['email'], hashed_pw)
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

        user = self.__repository.find_user_by_email(data['email'])

        if user is not None:
            if check_password_hash(user.password, data['password']):

                token = jwt.encode({
                    'email': data['email'],
                    'expiration': str(datetime.utcnow() + timedelta(minutes=30))
                },
                    os.getenv("SECRET_KEY"),
                    algorithm='HS256')

                response = {'token': token}
                return response


        return {'token': ''}

    def get_recordings_for_user(self, data):
        user = self.__repository.find_user_by_email(data['email'])

        if user is not None:

            recordings = self.__repository.get_recordings_for_user(data['email'])

            return recordings

        else:

            return {'Message': 'No user with the given email address'}

