from flask import jsonify, request
from functools import wraps
import os
import jwt

from .models.user_model import UserModel

def jwt_required(function): # original function is passed in
    @wraps(function)
    def wrap(*args, **kwargs):
        try: # check if token was sent
            token = request.headers.get('Authorization')
            data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms="HS256") # decodes token 
            user = UserModel.get_by_id(data['sub']) # get user

        except Exception as e: # maybe no token or no user found
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
    