from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv
import openai

load_dotenv()


class Openai(OpenaiProvider):
    NAME = "openai"
    API_KEY = os.environ["OPENAI_API_KEY"]
    HTTP_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_BASE_URL = "https://api.openai.com/v1"
    SUPPORTED_MODELS = {
        "gpt-4": "gpt-4",
        "gpt-4-turbo": "gpt-4-turbo",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
    }
