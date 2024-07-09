from providers.abstract_providers.base_provider import BaseProvider


class Groq(BaseProvider):
    ADAPTER_MODEL_STR_MAP = {
        "llama-3-8b-chat": "meta-llama/llama3-8b-8192",
        "llama-3-70b-chat": "meta-llama/llama3-70b-8192",
        "mixtral-8x7b": "mistralai/mixtral-8x7b-32768",
        "gemma-7b-instruct": "google/gemma-7b-it",
    }
    PROVIDER_NAME = "Groq"
