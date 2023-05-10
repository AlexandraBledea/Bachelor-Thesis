from flask import request, jsonify
from flask_restful import Resource
from database import db, Recording


class EmotionView(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']
        self.__first_model = kwargs['first-model']
    def post(self):
        data = request.get_json()

        result, bytes_plot = self.__first_model.execute(data['audio'], data['actualEmotion'])

        new_recording = Recording(data['actualEmotion'], result, bytes(data['audio']), data['model'], data['userEmail'],
                                  bytes_plot)

        db.session.add(new_recording)
        db.session.commit()
        db.session.flush()

        response = {'Emotion': result}
        return jsonify(response)