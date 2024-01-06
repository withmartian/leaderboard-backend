from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Decart(OpenaiProvider):
    NAME = "decart"
    API_KEY = os.environ["DECART_API_KEY"]
    HTTP_URL = "https://api.decart.ai/v1/chat/completions"
    OPENAI_BASE_URL = "https://api.decart.ai/v1/"
    SUPPORTED_MODELS = {
        "llama-2-70b-chat": "meta-llama/Llama-2-70b-chat-hf",
    }
