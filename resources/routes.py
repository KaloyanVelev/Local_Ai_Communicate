from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from utils.database import db
from utils.auth import auth
from models.user import UserModel
from schemas.user import UserCreationSchema, UserLogInSchema
from managers.user import UserManager

app_bp = Blueprint('api', __name__)


@auth.verify_token
def verify_token(token):
    user_id = UserModel.decode_token(token)
    return UserModel.query.filter_by(id=user_id).first() if user_id else None


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