import requests
from dotenv import load_dotenv
import os
from services.LMStudio import LMStudioService
from services.Ollama import OllamaService


llm_service = LMStudioService() #choose LMStudioService or OllamaService im working on making it easier!

#        / \
#         |
#         |