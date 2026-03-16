import requests
from dotenv import load_dotenv
import os

load_dotenv()

LMSTUDIO_BASE_URL = os.getenv('LMSTUDIO_BASE_URL') # LMStudio service URL


class LMStudioService:
    def __init__(self, model_name: str = 'qwen/qwen3.5-9b'):
        self.model_name = model_name
        self.url = f"{LMSTUDIO_BASE_URL}/v1/chat/completions"

    def chat(self,user_message,system_prompt = None):
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": user_message
        })
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=payload, timeout=300)
            response.raise_for_status()

            data = response.json()
            content = data['choices'][0]['message']['content']
            if not content:
                raise Exception(f"LMStudio returned empty content: {data}")

            return content
        except requests.exceptions.ConnectionError:
            raise Exception("LMStudio service is not running")
        except requests.exceptions.Timeout:
            raise Exception("LMStudio service timed out")
        except Exception as e:
            raise Exception(f"LLM error: {str(e)}")