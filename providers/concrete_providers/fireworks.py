from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Fireworks(OpenaiProvider):
    NAME = "fireworks"
    API_KEY = os.environ["FIREWORKS_API_KEY"]
    HTTP_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
    OPENAI_BASE_URL = "https://api.fireworks.ai/inference/v1"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "accounts/fireworks/models/mixtral-8x7b-instruct",
        "llama-2-70b-chat": "accounts/fireworks/models/llama-v2-70b-chat",
    }
