from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash

import app
from database import db, User


class RegisterView(Resource):

    def post(self):
        data = request.get_json()
        user = db.session.query(User).filter(User.email == data['email']).first()

        if user is None:
            hashed_pw = generate_password_hash(data['password'], "sha256")

            new_user = User(data['firstname'], data['lastname'], data['gender'], data['email'], hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            db.session.flush()

            response = {'Message': 'Account created successfully!'}
            return jsonify(response)
        else:
            response = {'Message': 'There exists an account with the given email!'}
            return jsonify(response)
