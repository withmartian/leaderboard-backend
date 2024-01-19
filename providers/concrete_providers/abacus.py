from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Abacus(OpenaiProvider):
    NAME = "Abacus"
    API_KEY = os.environ["ABACUS_API_KEY"]
    # HTTP_URL = ""
    OPENAI_BASE_URL = "https://llmapis.abacus.ai/api/compat/oai/v1"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "mixtral-8x7b",
    }
