from flask import jsonify, request
from functools import wraps
import os
import jwt

from .models.user_model import UserModel

def jwt_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms="HS256")
            user = UserModel.get_by_id(data['sub'])
        except Exception as e:
            # headers = {'Content-Type': 'application/json'}
            return jsonify({'message' : 'Token is invalid!'}), 401
        
        try:
            data = request.get_json()
        except:
            data = None

        return function(
            user = user,
            data=data,
            *args, 
            **kwargs) #keep this out of TRY block to prevent hiding errors from function

    return wrap
    