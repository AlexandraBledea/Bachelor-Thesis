from flask import request, jsonify
from flask_restful import Resource
from database import db, Recording
from flask_jwt_extended import jwt_required

from models.Strategy import Strategy


class EmotionViewSimple(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']
        self.__english_tess_model = kwargs['english_tess_model']
        self.__english_ravdess_model = kwargs['english_ravdess_model']

    @jwt_required()
    def post(self):
        data = request.get_json()

        print(data['model'])

        if data['model'] == "English Tess":
            self.__service.set_strategy(self.__english_tess_model)
        elif data['model'] == "English Ravdess":
            self.__service.set_strategy(self.__english_ravdess_model)

        result, bytes_plot = self.__service.predict_emotion(data['audio'], data['actualEmotion'])

        recording = self.__service.add_recording(data, result, bytes_plot).json()

        return jsonify(recording)
