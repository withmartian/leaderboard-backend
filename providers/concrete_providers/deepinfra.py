from providers.abstract_providers.openai_provider import OpenaiProvider
import os
from dotenv import load_dotenv

load_dotenv()


class Deepinfra(OpenaiProvider):
    NAME = "Deepinfra"
    API_KEY = os.environ["DEEPINFRA_API_KEY"]
    HTTP_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
    OPENAI_BASE_URL = "https://api.deepinfra.com/v1/openai"
    SUPPORTED_MODELS = {
        "mixtral-8x7b": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "llama2-70b-chat": "meta-llama/Llama-2-70b-chat-hf",
    }
