from flask import jsonify, json
from flask_jwt_extended import jwt_required
from flask_restful import Resource


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json'}


class RecordingsView(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']

    @jwt_required()
    def get(self):
        result = self.__service.get_recordings()
        return jsonify(result)
