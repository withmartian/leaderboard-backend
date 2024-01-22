from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Decart(OpenaiProvider):
    NAME = "Decart"
    API_KEY = os.environ["DECART_API_KEY"]
    OPENAI_BASE_URL = "https://api.decart.ai/v1/"
    SUPPORTED_MODELS = {
        "llama2-70b-chat": "meta-llama/llama-2-70b-chat-hf",
    }
