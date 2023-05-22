import ast
import base64
import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    __table_args__ = (
        db.UniqueConstraint('email'),
    )

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    gender = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    recordings = db.relationship('Recording', backref='user')

    def __init__(self, firstname, lastname, gender, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.firstname, self.lastname, self.gender, self.email}>"

    def json(self):
        recordings_data = [recording.json() for recording in self.recordings]
        return {"firstname": self.firstname, "lastname": self.lastname, "gender": self.gender, "email": self.email,
                'recordings': recordings_data}


class Recording(db.Model):
    __tablename__ = 'recording'

    id = db.Column(db.Integer, primary_key=True)
    actual_emotion = db.Column(db.String())
    predicted_emotion = db.Column(db.String())
    audio = db.Column(db.LargeBinary())
    model = db.Column(db.String())
    email = db.Column(db.String(), db.ForeignKey('user.email'))
    statistics = db.Column(db.String())

    def __init__(self, actual_emotion, predicted_emotion, audio, model, email, statistics):
        self.actual_emotion = actual_emotion
        self.predicted_emotion = predicted_emotion
        self.audio = audio
        self.model = model
        self.email = email
        self.statistics = statistics

    def json(self):
        audio_numbers = [x for x in self.audio]

        # string = self.statistics_percentages.strip('{}')
        # statistics_percentages = [round(float(num), 2) for num in string.split(',')]
        #
        # string = self.statistics_labels.strip('{}')
        # statistics_labels = string.split(',')

        return {"email": self.email, "actualEmotion": self.actual_emotion, "predictedEmotion": self.predicted_emotion,
                "audio": audio_numbers,
                "model": self.model, "statistics": eval(self.statistics)}


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db
