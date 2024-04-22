import os
from dotenv import load_dotenv

from ..abstract_providers.openai_provider import OpenaiProvider


load_dotenv()


class Abacus(OpenaiProvider):
    NAME = "Abacus"
    API_KEY = os.environ["ABACUS_API_KEY"]
    OPENAI_BASE_URL = "https://llmapis.abacus.ai/api/compat/oai/v1"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "mixtral-8x7b",
    }
