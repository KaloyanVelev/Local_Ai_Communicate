import uuid
from database import db
from models.enums import UserLevel
from sqlalchemy import func

class AIChatHistoryModel(db.Model):
    __tablename__ = 'ai_chats'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    query_content = db.Column(db.Text(), nullable=False)
    response = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel', backref='ai_chats')
