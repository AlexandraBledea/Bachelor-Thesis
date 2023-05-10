from flask import Flask, render_template, session, request, jsonify
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from database import *
from flask_restful import Api, Resource
from flask_cors import CORS
from functools import wraps

from werkzeug.security import check_password_hash, generate_password_hash
from models.EnglishModel import FirstModel
from service.service import Service

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
service = Service(db)
first_model = FirstModel()


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


# Wrapper function to apply the decorator to the resource
def token_required_resource(resource):
    resource.post = token_required(resource.post)
    return resource


@token_required
@app.route('/login/change-password', methods=['PUT'])
def put_change_password():
    data = request.get_json()
    response = service.change_password(data)
    return jsonify(response)


@token_required
@app.route('/login', methods=['POST'])
def post_login():
    data = request.get_json()
    response = service.login(data)
    if response['token'] != '':
        session['logged_in'] = True
        return jsonify(response)

    return jsonify(response)


@token_required
@app.route('/register', methods=['POST'])
def post_register():
    data = request.get_json()
    response = service.register_user(data)
    return jsonify(response)


@token_required
@app.route('/get-prediction', methods=['POST'])
def post_predict():
    data = request.get_json()

    result, bytes_plot = first_model.execute(data['audio'], data['actualEmotion'])

    new_recording = Recording(data['actualEmotion'], result, bytes(data['audio']), data['model'], data['userEmail'],
                              bytes_plot)

    db.session.add(new_recording)
    db.session.commit()
    db.session.flush()

    response = {'Emotion': result}
    return jsonify(response)


@token_required
@app.route('/get-recodings', methods=['POST'])
def post_get_recordings():
    data = request.get_json()
    result = service.get_recordings_for_user()
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)

# class UserView(Resource):
#
#     @token_required
#     def get(self):
#         users = db.session.query(User).all()
#         return {'Users': list(x.json() for x in users)}
#
#
# @app.route('/unprotected')
# def unprotected():
#     return jsonify({'message': 'Anyone can view this!'})
#
#
# @app.route('/protected')
# @token_required
# def protected():
#     return jsonify({'message': 'This is only available for people with valid token!'})
#

# @app.route('/')
# def home():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         return 'Logged in currently!'
#
#     return app



