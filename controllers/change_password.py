from datetime import datetime, timedelta

import jwt
from flask import request, jsonify, session
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from database import db, User

from dotenv import load_dotenv
import os


class ChangePasswordView(Resource):

    def put(self):
        data = request.get_json()
        user = db.session.query(User).filter(User.email == data['email']).first()

        if user is not None:
            if check_password_hash(user.password, data['oldPassword']):
                hashed_pw = generate_password_hash(data['newPassword'], "sha256")

                user.password = hashed_pw
                db.session.commit()
                db.session.flush()

                response = {'Message': 'Password changed successfully!'}
                return jsonify(response)
            else:
                response = {'Message': 'Invalid password or email'}
                return jsonify(response)
        else:
            response = {'Message': 'Invalid password or email'}
            return jsonify(response)
