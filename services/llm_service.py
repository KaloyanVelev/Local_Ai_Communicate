import requests
from dotenv import load_dotenv
import os
from services.lmstudio import LMStudioService
from services.ollama import OllamaService


llm_service = LMStudioService() #choose LMStudioService or OllamaService im working on making it easier!

#        / \
#         |
#         |