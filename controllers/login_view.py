from flask import request, jsonify, session
from flask_cors import cross_origin
from flask_restful import Resource


class LoginView(Resource):

    def __init__(self, **kwargs):
        self.__service = kwargs['service']

    @cross_origin()
    def post(self):
        data = request.get_json()
        response = self.__service.login(data)
        if response['token'] != '':
            session['logged_in'] = True
            return jsonify(response)

        return jsonify(response)
