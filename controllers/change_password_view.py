from flask import request, jsonify, session
from flask_restful import Resource


class ChangePasswordView(Resource):
    def __init__(self, **kwargs):
        self.__service = kwargs['service']

    def put(self):
        data = request.get_json()
        response = self.__service.change_password(data)
        return jsonify(response)

