from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Perplexity(OpenaiProvider):
    NAME = "perplexity"
    API_KEY = os.environ["PERPLEXITY_API_KEY"]
    HTTP_URL = "https://api.perplexity.ai/chat/completions"
    OPENAI_BASE_URL = "https://api.perplexity.ai"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "mistral-7b-instruct",
        "llama-2-70b-chat": "llama-2-70b-chat",
    }
