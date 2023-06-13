

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class CheckConnection(Resource):

    @jwt_required()
    def post(self):
        response = {"msg": "ok!"}
        return jsonify(response)
