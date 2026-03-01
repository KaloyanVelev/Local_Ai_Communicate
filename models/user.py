import uuid
from utils.database import db
from models.enums import UserLevel

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    permission = db.Column(db.String(40), default=UserLevel.BASIC_USER.name)
