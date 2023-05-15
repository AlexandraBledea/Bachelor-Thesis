

from flask import jsonify
from flask_restful import Resource


class CheckConnection(Resource):

    def post(self):
        response = {"msg": "ok!"}
        return jsonify(response)
