import os
from flask import jsonify, request, session
import jwt
from app import app
from app.decorators import jwt_required

from flask_pyjwt import AuthManager

from app.models.user_model import UserModel

def get_user_object(user):
    return {
        "id": user.id
    }

@app.route('/user/register', methods=['POST'])
def register():
    user_data = request.get_json()

    registration_errors = UserModel.validate_registration_data(user_data)
    if len(registration_errors) > 0:
        return jsonify(
            {
                'errors': registration_errors
            }
        ), 422

    new_user = UserModel.add_user(user_data)
    if new_user is None:
        return jsonify(
            {
                'resuilt': 'invalid'
            }
        ), 400
    
    return jsonify(), 200

@app.route('/user/login', methods=['POST'])
def login():
    
    credentials = request.get_json()
    user = UserModel.login(credentials)

    if user is None:
        return jsonify({}), 401

    auth_manager = AuthManager(app)
    return jsonify({
            'auth_token':auth_manager.auth_token(user.id, {}).signed,
            'user': user.to_json()
        }) , 200

@app.route('/user/logout')
def logout():
    return jsonify ({}), 200

@app.route('/user/current-user')
@jwt_required
def get_current_user(user, *args, **kwargs): 
    # called when user reloads the app. Their TOKENS are good, just need to get the up-to-date user data
    return jsonify(get_user_object(user)) , 200

@app.route('/user/refresh-token', methods=['POST'])
def refresh_token(*args, **kwargs):

    auth_manager = AuthManager(app)

    try:
        data = request.get_json()
        data = jwt.decode(data['refresh'], os.getenv('JWT_SECRET'), algorithms="HS256")
        user = UserModel.get_by_id(data['sub'])

        if user is None:
            return jsonify({
                'auth_token': None,
                'refresh_token': None
                }) , 200

        return jsonify({
            'auth_token':auth_manager.auth_token(user.id, {}).signed,
            'refresh_token': auth_manager.refresh_token(user.id).signed,
            }) , 200
    
    except Exception as e:
        return jsonify({}), 401
