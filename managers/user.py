from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from utils.database import db
from models.user import UserModel
from schemas.user import UserCreationSchema, UserLogInSchema
from managers.auth import AuthManager


class UserManager:
    @staticmethod
    def register(provided_data):
        if not provided_data:
            return {'error': 'No data provided'}
        errors =UserCreationSchema().validate(provided_data)
        if errors:
            return jsonify(errors)

        username = provided_data['username']
        email = provided_data['email']
        password = provided_data['password']

        user = UserModel(username=username,email=email,password=generate_password_hash(password))

        db.session.add(user)
        db.session.commit()
        return {
            'message': f'Added User named: {username}'
        }

    @staticmethod
    def login(provided_data):
        if not provided_data:
            return {
                "error": "No data given"
            }, 400
        errors = UserLogInSchema().validate(provided_data)
        if errors:
            return jsonify(errors)
        user = UserModel.query.filter_by(username=provided_data['username']).first()
        if not user:
            return {'error': 'User not found'},400
        if not check_password_hash(user.password,provided_data['password']):
            return jsonify({"error": "invalid password"}), 400
        token = AuthManager.encode_token(user)
        return {
            "message": "login successful!",
            "token": token,
            "user_id": user.id,
            "Permission Level": user.permission
        }


    @staticmethod
    def get_private_info(user_object):
        return {
            'message': f'Hello {user_object.username} your permission is: {user_object.permission}'
        }

