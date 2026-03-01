from flask import Blueprint, request
from utils.auth import auth
from managers.user import UserManager

app_bp = Blueprint('api', __name__)

@app_bp.route('/login', methods=['POST'])
def user_login():
    provided_data = request.json
    return UserManager.login(provided_data)


@app_bp.route('/register', methods=['POST'])
def create_user():
    provided_data = request.json

    return UserManager.register(provided_data)


@app_bp.route('/secret', methods=["GET"])
@auth.login_required
def get_private_info():
    user = auth.current_user()
    return UserManager.get_private_info(user)


@app_bp.route('/')
def test():
    return '<p>Database connected</p>'