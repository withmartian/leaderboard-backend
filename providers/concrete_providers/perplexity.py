from providers.abstract_providers.base_provider import BaseProvider


class Perplexity(BaseProvider):
    ADAPTER_MODEL_STR_MAP = {
        "llama-3-8b-chat": "perplexity/llama-3-8b-instruct",
        "llama-3-70b-chat": "perplexity/llama-3-70b-instruct",
        "mixtral-8x7b": "perplexity/mixtral-8x7b-instruct",
    }
    PROVIDER_NAME = "Perplexity"
