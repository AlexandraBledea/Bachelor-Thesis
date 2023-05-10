from datetime import datetime, timedelta

import jwt
from flask import request, jsonify, session
from flask_restful import Resource, Api
from werkzeug.security import check_password_hash, generate_password_hash

from database import db, User, Recording

from dotenv import load_dotenv
import os

from models.EnglishModel import FirstModel
from service.service import Service

