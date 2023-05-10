from flask import request, jsonify
from flask_restful import Resource


class RecordingsView(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']

    def get(self):
        data = request.get_json()
        result = self.__service.get_recordings_for_user()
        return jsonify(result)
