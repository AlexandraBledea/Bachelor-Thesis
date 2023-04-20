from datetime import datetime, timedelta

import jwt
from flask import request, jsonify, session
from flask_restful import Resource
from werkzeug.security import check_password_hash

from database import db, User

from dotenv import load_dotenv
import os


class LoginView(Resource):

    def post(self):
        data = request.get_json()
        user = db.session.query(User).filter(User.email == data['email']).first()

        if user is not None:
            if check_password_hash(user.password, data['password']):
                session['logged_in'] = True

                token = jwt.encode({
                    'email': data['email'],
                    'expiration': str(datetime.utcnow() + timedelta(minutes=30))
                },
                    os.getenv("SECRET_KEY"),
                    algorithm='HS256')

                print(user.email)
                return jsonify({'token': token})

        return jsonify({'token': ''})
