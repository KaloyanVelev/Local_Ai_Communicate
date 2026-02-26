import uuid
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
from utils.database import db
from models.enums import UserLevel

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    permission = db.Column(db.String(40), default=UserLevel.BASIC_USER.name)

    def encode_token(self):
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=1),
            'sub': self.id
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None