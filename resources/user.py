from flask import request
from flask_restful import Resource
from managers.auth import auth
from managers.user import UserManager
from schemas.request.auth import UserLogInSchema, UserCreationSchema
from utils.decorator import validate_schema,permission_required


class UserRegisterResource(Resource):
    @validate_schema(UserCreationSchema)
    def post(self):
        provided_data = request.json
        return UserManager.register(provided_data)


class UserLogInResource(Resource):
    @validate_schema(UserLogInSchema)
    def post(self):
        provided_data = request.json
        return UserManager.login(provided_data)

class UserPrivateInfoResource(Resource):
    @auth.login_required
    def get(self):
        user = auth.current_user()
        return UserManager.get_private_info(user)


class UserPlanUpgradeResource(Resource):
    @auth.login_required
    def post(self):
        user = auth.current_user()
        provided_data = request.json
        return UserManager.plan_upgrade(user, provided_data['upgrade_to'])

class ShowUsersResource(Resource):
    @auth.login_required
    @permission_required('ADMIN_USER')
    def get(self):
        return UserManager.show_users()


class TestResource(Resource):
    def get(self):
        return '<p>Database connected</p>'