from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class EmotionViewSimple(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']

    @jwt_required()
    def post(self):
        data = request.get_json()

        model_name, prediction = self.__service.find_best_prediction(data['audio'])

        recording = self.__service.add_recording(data['actualEmotion'], data['audio'], model_name,
                                                 data['userEmail'], prediction.capitalize(), []).json()

        return jsonify(recording)
