from flask import request, jsonify
from flask_restful import Resource


class RegisterView(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']


    def post(self):
        data = request.get_json()
        response = self.__service.register_user(data)
        return jsonify(response)