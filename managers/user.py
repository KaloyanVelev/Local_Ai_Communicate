from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from models.user import UserModel
from managers.auth import AuthManager
from models.enums import UserLevel
from sqlalchemy import func


class UserManager:
    @staticmethod
    def register(provided_data):
        if UserModel.query.filter_by(email=provided_data['email']).first():
            raise ValueError('Email already registered')

        provided_data['password'] = generate_password_hash(provided_data['password'])

        user = UserModel(**provided_data)

        db.session.add(user)
        db.session.commit()
        return {
            'message': f'Added User named: {user.username}'
        },200

    @staticmethod
    def login(provided_data):
        user = UserModel.query.filter_by(username=provided_data['username']).first()
        if not user or not check_password_hash(user.password,provided_data['password']):
            return jsonify({"error": "invalid credentials"}), 400
        token = AuthManager.encode_token(user)
        return {
            "message": "login successful!",
            "token": token,
            "user_id": user.id,
            "Permission Level": user.permission
        }, 200


    @staticmethod
    def get_private_info(user_object):
        return {
            'message': f'Hello {user_object.username} your permission is: {user_object.permission}'
        }, 200

    @staticmethod
    def plan_upgrade(user, upgrade_to):
        if upgrade_to in UserLevel:
            user.permission = upgrade_to
            user.updated_on = func.now()
            db.session.commit()
            return {
                'message': f'User {user.username} upgraded to {upgrade_to}'
            }, 200
        return {'error': 'Invalid upgrade level'}, 400

    @staticmethod
    def show_users():
        users = UserModel.query.all()

        return {
            'message': f'Users: {len(users)}'
        }, 200
