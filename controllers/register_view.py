from flask import request, jsonify
from flask_cors import cross_origin
from flask_restful import Resource


class RegisterView(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']

    @cross_origin()
    def post(self):
        data = request.get_json()
        response = self.__service.register_user(data)
        return jsonify(response)