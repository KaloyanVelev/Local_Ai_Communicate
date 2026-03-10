from flask import request, jsonify
from flask_restful import Resource
from managers.auth import auth
from managers.chat_history import ChatHistoryManager
from schemas.request.ai import AISchema
from services.llm_service import llm_service
from utils.decorator import permission_required

LLM_PROMPT = "You are a helpful assistant. That does whatever the user asks."


class AIChatResource(Resource):
    @auth.login_required
    def post(self):
        current_user = auth.current_user()
        data = request.json
        schema = AISchema()
        errors = schema.validate(data)
        if errors:
            return{'message': errors}, 400
        try:
            response = llm_service.chat(
                user_message=data['query'],
                system_prompt=LLM_PROMPT
            )

            ChatHistoryManager.save(
                user_id=current_user.id,
                query_content=data['query'],
                response=response
            )
            return {'response': response}, 200
        except Exception as e:
            return {'message': str(e)}, 500
    @auth.login_required
    def get(self):
        current_user = auth.current_user()
        return ChatHistoryManager.get_history(current_user.id), 200


class ChatHistoryResource(Resource):
    @auth.login_required
    @permission_required('ADMIN_USER')
    def get(self):
        return ChatHistoryManager.get_all_history(), 200





