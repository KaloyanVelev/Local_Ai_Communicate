from flask import Blueprint, request
from managers.auth import auth
from managers.user import UserManager
from schemas.request.auth import UserLogInSchema, UserCreationSchema
from utils.decorator import validate_schema,permission_required

app_bp = Blueprint('api', __name__)

@app_bp.route('/login', methods=['POST'])
@validate_schema(UserLogInSchema)
def user_login():
    provided_data = request.json
    return UserManager.login(provided_data)


@app_bp.route('/register', methods=['POST'])
@validate_schema(UserCreationSchema)
def create_user():
    provided_data = request.json
    return UserManager.register(provided_data)


@app_bp.route('/secret', methods=["GET"])
@auth.login_required
def get_private_info():
    user = auth.current_user()
    return UserManager.get_private_info(user)

@app_bp.route('/planUpgrade', methods=["POST"])
@auth.login_required
def plan_upgrade():
    user = auth.current_user()
    provided_data = request.json
    return UserManager.plan_upgrade(user, provided_data['upgrade_to'])

@app_bp.route('/showusers', methods=["GET"])
@auth.login_required
@permission_required('ADMIN_USER')
def show_users():
    return UserManager.show_users()
@app_bp.route('/')
def test():
    return '<p>Database connected</p>'