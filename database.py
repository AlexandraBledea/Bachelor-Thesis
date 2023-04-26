from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    gender = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, firstname, lastname, gender, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.firstname, self.lastname, self.gender, self.email}>"

    def json(self):
        return {"firstname": self.firstname, "lastname": self.lastname, "gender": self.gender, "email": self.email}


class Recording(db.Model):
    __tablename__ = 'recording'

    id = db.Column(db.Integer, primary_key=True)
    actual_emotion = db.Column(db.String())
    predicted_emotion = db.Column(db.String())
    audio = db.Column(db.LargeBinary())
    model = db.Column(db.String())

    def __init__(self, actual_emotion, predicted_emotion, audio, model):
        self.actual_emotion = actual_emotion
        self.predicted_emotion = predicted_emotion
        self.audio = audio
        self.model = model

    def json(self):
        return {"actual_emotion": self.actual_emotion, "predicted_emotion": self.predicted_emotion, "audio": self.audio,
                "model": self.model}


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db
