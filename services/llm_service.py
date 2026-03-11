import requests

OLLAMA_BASE_URL = "http://localhost:11434" # Ollama service URL
LMSTUDIO_BASE_URL = "http://localhost:1234" # LMStudio service URL

#choose one of the services at the end of the file

class OllamaService:
    def __init__(self, model_name: str = 'qwen3.5:9b'):
        self.model_name = model_name
        self.url = f"{OLLAMA_BASE_URL}/api/chat"

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
            response = requests.post(self.url, json=payload, timeout=45)
            response.raise_for_status()

            data = response.json()
            content = data.get("message", {}).get("content", "").strip()
            if not content:
                raise Exception(f"Ollama returned empty content: {data}")

            return content
        except requests.exceptions.ConnectionError:
            raise Exception("Ollama service is not running")
        except requests.exceptions.Timeout:
            raise Exception("Ollama service timed out")
        except Exception as e:
            raise Exception(f"LLM error: {str(e)}")

class LMStudioService:
    def __init__(self, model_name: str = 'qwen3.5:9b'):
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




llm_service = LMStudioService() #choose LMStudioService or OllamaService im working on making it easier!