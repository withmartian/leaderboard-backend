from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Anyscale(OpenaiProvider):
    NAME = "Anyscale"
    API_KEY = os.environ["ANYSCALE_API_KEY"]
    OPENAI_BASE_URL = "https://api.endpoints.anyscale.com/v1"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "llama2-70b-chat": "meta-llama/Llama-2-7b-chat-hf",
    }
