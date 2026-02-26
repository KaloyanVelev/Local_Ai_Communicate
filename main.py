from enum import Enum
from marshmallow import Schema, fields, validate
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
import jwt
import uuid
from datetime import datetime, timedelta, timezone

class UserLevel(Enum):
    BASIC_USER = "Basic"
    PLUS_USER = "Plus"
    PRO_USER = "Pro"
    ENTERPRISE_USER = "Enterprise"
    ADMIN_USER = "Admin"

db_user = 'postgres'
db_password = '2011'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5432/postgres'

db = SQLAlchemy(app)
api = Api(app)
auth = HTTPTokenAuth(scheme='Bearer')

app.config['SECRET_KEY'] = "52f0c854e544f440769cba3b9c4405bd8d791f0dd5c6d5a3673eba39146bec40"


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(40), primary_key=True, default = lambda: str(uuid.uuid4()))
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    permission = db.Column(db.String(40), default=UserLevel.BASIC_USER.name)

    def encode_token(self):
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=1),
            'sub': self.id
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

@auth.verify_token
def verify_token(token):
    user_id = UserModel.decode_token(token)
    return  UserModel.query.filter_by(id=user_id).first() if user_id else None

class BaseUserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=4, max=40))

class UserCreationSchema(BaseUserSchema):
    email = fields.Email(required=True, validate=validate.Length(min=5, max=40))
    password = fields.String(required=True, validate=validate.Length(min=5,max = 255))

class UserLogInSchema(BaseUserSchema):
    password = fields.String(required=True, validate=validate.Length(min=5,max = 255))

@app.route('/login', methods = ['POST'])
def user_login():
    provided_data = request.json
    if not provided_data:
        return jsonify({"error": "No data given"}), 400
    errors = UserLogInSchema().validate(provided_data)
    if errors:
        return jsonify(errors), 400
    user = UserModel.query.filter_by(username = provided_data['username']).first()
    if not user:
        return jsonify({"error": "User not found"}), 400
    if not check_password_hash(user.password, provided_data['password']):
        return jsonify({"error":"invalid password"}), 400

    token = user.encode_token()

    return jsonify({
    "message" : "login successful!",
    "token" : token,
    "user_id" : user.id,
    "Permission Level": user.permission})


@app.route('/register', methods=['POST'])
def create_user():
    provided_data = request.json
    if not provided_data:
        return jsonify({"error": "No data provided"}), 400

    errors =UserCreationSchema().validate(provided_data)
    if errors:
        return jsonify(errors), 400

    username = provided_data['username']
    email = provided_data['email']
    password = provided_data['password']

    user = UserModel(username=username, email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return jsonify(f"Added User named:[{username}]!!")

@app.route('/secret', methods = ["GET"])
@auth.login_required()
def get_private_info():
    user = auth.current_user()
    return jsonify({"message" : f"Hello {user.username} your permission level is: {user.permission}",})

@app.route('/')
def test():
    return '<p>Database connected</p>'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)