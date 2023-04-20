from flask import Flask, render_template, session, request, jsonify
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from database import *
from flask_restful import Api, Resource
import jwt
from datetime import datetime
from flask_cors import CORS
from functools import wraps
from controllers.register import RegisterView
from controllers.login import LoginView
from controllers.change_password import ChangePasswordView

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + os.getenv("DB_USER") + \
                                        ':' + os.getenv("DB_PASSWORD") + '@' + \
                                        os.getenv("DB_HOST") + '/' + os.getenv("DB_NAME")

db = init_app(app)
api = Api(app)
CORS(app)
Migrate(app, db)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return jsonify({'Token': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if datetime.utcnow() > datetime.strptime(data["expiration"], "%Y-%m-%d %H:%M:%S.%f"):
                print("JWT has expired")
                return jsonify({'Token': 'token has expired'})

            current_user = db.session.query(User).filter(User.email == data['email']).first()
        except:
            return jsonify({'Message': 'token is invalid'})

        return f(*args, **kwargs)

    return decorator


class UserView(Resource):

    @token_required
    def get(self):
        users = db.session.query(User).all()
        return {'Users': list(x.json() for x in users)}


@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is only available for people with valid token!'})


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently!'

    return app


api.add_resource(UserView, '/users')
api.add_resource(RegisterView, '/register')
api.add_resource(LoginView, '/login')
api.add_resource(ChangePasswordView, '/login/change-password')


if __name__ == '__main__':
    app.run(debug=True)
