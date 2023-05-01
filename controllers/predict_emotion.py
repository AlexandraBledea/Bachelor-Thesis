from flask import request, jsonify
from flask_restful import Resource

from database import db, Recording

from models.FirstModel import FirstModel


class EmotionView(Resource):

    def __init__(self):
        self.__first_model = FirstModel()

    def post(self):
        data = request.get_json()

        result = self.__first_model.receive_recording(data['audio'], data['actualEmotion'])

        new_recording = Recording(data['actualEmotion'], result, bytes(data['audio']), data['model'])

        db.session.add(new_recording)
        db.session.commit()
        db.session.flush()

        response = {'Emotion': result}
        return jsonify(response)
