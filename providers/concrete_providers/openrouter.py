from providers.abstract_providers.base_provider import BaseProvider


class OpenRouter(BaseProvider):
    ADAPTER_MODEL_STR_MAP = {
        "dbrx-instruct": "databricks/dbrx-instruct",
        "llama-3-8b-chat": "meta-llama/llama-3-8b-instruct",
        "llama-3-70b-chat": "meta-llama/llama-3-70b-instruct",
        "mixtral-8x7b": "mistralai/mixtral-8x7b-instruct",
        "mixtral-8x22b": "mistralai/mixtral-8x22b-instruct",
        "mistral-7b-chat": "mistralai/mistral-7b-instruct",
        "gemma-7b-instruct": "google/gemma-7b-it",
    }
    PROVIDER_NAME = "OpenRouter"
