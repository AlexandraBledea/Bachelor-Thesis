from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class EmotionViewExpert(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']

    @jwt_required()
    def post(self):
        data = request.get_json()

        result, statistics = self.__service.predict_emotion(data['model'], data['audio'])

        recording = self.__service.add_recording(data['actualEmotion'], data['audio'], data['model'],
                                                 data['userEmail'], result.capitalize(), statistics).json()

        return jsonify(recording)
