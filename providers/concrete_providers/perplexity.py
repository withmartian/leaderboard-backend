from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Perplexity(OpenaiProvider):
    NAME = "Perplexity"
    API_KEY = os.environ["PERPLEXITY_API_KEY"]
    HTTP_URL = "https://api.perplexity.ai/chat/completions"
    OPENAI_BASE_URL = "https://api.perplexity.ai"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "mixtral-8x7b-instruct",
        "llama2-70b-chat": "llama-2-70b-chat",
    }
