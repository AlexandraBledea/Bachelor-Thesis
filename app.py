from flask import Flask, render_template, session, request, jsonify
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from database import *
from flask_restful import Api, Resource
from flask_cors import CORS
from functools import wraps

from controllers.change_password_view import ChangePasswordView
from controllers.login_view import  LoginView
from controllers.predict_emotion_view_expert_user import EmotionViewExpert
from controllers.register_view import RegisterView
from controllers.recordings_view import RecordingsView
from controllers.check_connection import CheckConnection

from werkzeug.security import check_password_hash, generate_password_hash
from models.EnglishModel import FirstModel
from service.service import Service
from models.EnglishTessModel import EnglishTessModel
from models.EnglishRavdessModel import EnglishRavdessModel

from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + os.getenv("DB_USER") + \
                                        ':' + os.getenv("DB_PASSWORD") + '@' + \
                                        os.getenv("DB_HOST") + '/' + os.getenv("DB_NAME")



# config_app(app, "flask_config.ini")
db = init_app(app)
jwt = JWTManager(app)
Migrate(app, db)
CORS(app)
api = Api(app)
service = Service(db)
first_model = FirstModel()
english_tess_model = EnglishTessModel()
english_ravdess_model = EnglishRavdessModel()

app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
# app.config["JWT_REQUIRED_CLAIMS"] = []


api.add_resource(CheckConnection, '/check-connection')

api.add_resource(LoginView, '/login', resource_class_kwargs={
    'service': service
})

api.add_resource(ChangePasswordView, '/login/change-password', resource_class_kwargs={
    'service': service
})

api.add_resource(RegisterView, '/register', resource_class_kwargs={
    'service': service
})

api.add_resource((EmotionViewExpert), '/get-prediction', resource_class_kwargs={
    'service': service,
    # 'first-model': first_model,
    'english_tess_model': english_tess_model,
    'english_ravdess_model': english_ravdess_model
})

api.add_resource((RecordingsView), '/recordings', resource_class_kwargs = {
    'service': service
})


if __name__ == '__main__':
    app.run(debug=True)
























# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#
#         token = None
#
#         if 'token' in request.headers:
#             token = request.headers['token']
#
#         if not token:
#             return jsonify({'Token': 'a valid token is missing'})
#
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#             if datetime.utcnow() > datetime.strptime(data["expiration"], "%Y-%m-%d %H:%M:%S.%f"):
#                 print("JWT has expired")
#                 return jsonify({'Token': 'token has expired'})
#
#             current_user = db.session.query(User).filter(User.email == data['email']).first()
#         except:
#             return jsonify({'Message': 'token is invalid'})
#
#         return f(*args, **kwargs)
#
#     return decorator
#
#
# # Wrapper function to apply the decorator to the resource
# def token_required_resource(resource):
#     if hasattr(resource, 'post'):
#         resource.post = token_required(resource.post)
#     elif hasattr(resource, 'get'):
#         resource.get = token_required(resource.get)
#     elif hasattr(resource, 'put'):
#         resource.put = token_required(resource.put)
#     return resource
