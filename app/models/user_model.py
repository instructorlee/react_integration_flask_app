from flask import flash, session
import re
from app import app
from flask_bcrypt import Bcrypt

from app.models.base_models import BaseModel       

from ..models.connector import MySQLConnection
 
bcrypt = Bcrypt(app)

class UserModel(BaseModel):

    table="users"
    json_fields = ['id', 'email']

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    def __init__(self, data):

        self.id = data['id']
        #self.created_at = data['created_at']
        #self.updated_at = data['updated_at']
        self.email = data['email']
        self.password = data['password'] if 'password' in data else None

    @classmethod
    def get_by_email(cls, email):
        t = cls.filter_one_by({'email': email})
        return cls.filter_one_by({'email': email})

    @classmethod
    def save(cls, user):
        
        query = """
            INSERT INTO users
                (   
                    email,
                    password
                )
            VALUES
                (
                    %(email)s,
                    %(password)s
                )
        """

        new_user_id = MySQLConnection(cls.db).query_db(query, user)

        return None if not new_user_id else cls.get_by_id(new_user_id)

    @classmethod
    def add_user(cls, user):
         return cls.save({
            "email": user['email'],
            "password": bcrypt.generate_password_hash(user['password'])
        })

    @classmethod
    def login(cls, user):

        found_user = UserModel.get_by_email(user['email'])
        if  found_user is not None:
            if bcrypt.check_password_hash(found_user.password, user['password']):
                session['user_id'] = found_user.id
                return found_user

        return None

    @classmethod
    def validate_registration_data(cls, user):

        errors = []
        
        if 'email' in user:
            if UserModel.get_by_email(user['email']) is not None:
                errors.append("That email is taken")

            if len(user['email']) == 0:
                errors.append("Email Required")

            elif not cls.EMAIL_REGEX.match(user['email']):
                errors.append("Invalid Email format")
        else:

            errors.append("Email Required")
        
        if 'password' in user and 'confirm_password' in user:
            if len(user['password']) < 8:
                errors.append("Password minimum 8 characters")

            if user['password'] != user['confirm_password']:
                errors.append("Passwords must match")
        else:
            errors.append("Password and confirm password required")

        return errors
