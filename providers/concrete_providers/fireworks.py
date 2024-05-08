from providers.abstract_providers.base_provider import BaseProvider


class Fireworks(BaseProvider):
    ADAPTER_MODEL_STR_MAP = {
        "dbrx-instruct": "accounts/fireworks/models/mistral-7b-instruct-v0p2",
        "llama-3-8b-chat": "accounts/fireworks/models/llama-v3-8b-instruct",
        "llama-3-70b-chat": "accounts/fireworks/models/llama-v3-70b-instruct",
        "mixtral-8x7b": "accounts/fireworks/models/mixtral-8x7b-instruct",
        "mixtral-8x22b": "accounts/fireworks/models/mixtral-8x22b-instruct",
        "mistral-7b-chat": "accounts/fireworks/models/mistral-7b-instruct-v0p2",
        "gemma-7b-instruct": "accounts/fireworks/models/gemma-7b-it",
    }
    PROVIDER_NAME = "Fireworks"
