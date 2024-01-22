from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from typing import Callable
from dotenv import load_dotenv

load_dotenv()


class Together(OpenaiProvider):
    NAME = "Together"
    API_KEY = os.environ["TOGETHER_API_KEY"]
    OPENAI_BASE_URL = "https://api.together.xyz/v1"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "llama2-70b-chat": "togethercomputer/llama-2-70b-chat",
    }

    def together_get_completion_tokens(response):
        return response["output"]["usage"]["completion_tokens"]
