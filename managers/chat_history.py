from flask import jsonify

from database import db
from models.ai import AIChatHistoryModel

class ChatHistoryManager:
    @staticmethod
    def save(user_id, query_content, response):
        entry =AIChatHistoryModel(
            user_id=user_id,
            query_content=query_content,
            response=response,
        )
        db.session.add(entry)
        db.session.commit()
        return entry
    @staticmethod
    def get_history(user_id):
        return [
            {
                "id": item.id,
                "query": item.query_content,
                "response": item.response,
                "created_on": item.created_on.isoformat() if item.created_on else None,
                "user_id": item.user_id,
            }
            for item in AIChatHistoryModel.query.filter_by(user_id=user_id).all()
        ]

    @staticmethod
    def get_all_history():
        return [
            {
                "id": item.id,
                "query": item.query_content,
                "response": item.response,
                "created_on": item.created_on.isoformat() if item.created_on else None,
                "user_id": item.user_id,
            }
            for item in AIChatHistoryModel.query.all()
        ]