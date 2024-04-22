import os
from dotenv import load_dotenv

from ..abstract_providers.openai_provider import OpenaiProvider


load_dotenv()


class Fireworks(OpenaiProvider):
    NAME = "Fireworks"
    API_KEY = os.environ["FIREWORKS_API_KEY"]
    OPENAI_BASE_URL = "https://api.fireworks.ai/inference/v1"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "accounts/fireworks/models/mixtral-8x7b-instruct",
        "llama2-70b-chat": "accounts/fireworks/models/llama-v2-70b-chat",
    }
