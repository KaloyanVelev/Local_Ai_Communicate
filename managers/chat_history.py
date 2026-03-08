from database import db
from models.ai import AIChatHistoryModel

class ChatHistoryManager:
    @staticmethod
    def save(user_id, query, response):
        entry =AIChatHistoryModel(
            user_id=user_id,
            query=query,
            response=response,
        )
        db.session.add(entry)
        db.session.commit()
        return entry