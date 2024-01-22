from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Openai(OpenaiProvider):
    NAME = "OpenAI"
    API_KEY = os.environ["OPENAI_API_KEY"]
    OPENAI_BASE_URL = "https://api.openai.com/v1"
    SUPPORTED_MODELS = {
        "gpt-4": "gpt-4",
        "gpt-4-turbo": "gpt-4-1106-preview",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
    }
