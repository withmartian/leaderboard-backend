from providers.abstract_providers.base_provider import BaseProvider


class Together(BaseProvider):
    ADAPTER_MODEL_STR_MAP = {
        "dbrx-instruct": "databricks/dbrx-instruct",
        "llama-3-8b-chat": "meta-llama/Llama-3-8b-chat-hf",
        "llama-3-70b-chat": "meta-llama/Llama-3-70b-chat-hf",
        "mixtral-8x7b": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mixtral-8x22b": "mistralai/Mixtral-8x22B-Instruct-v0.1",
        "mistral-7b-chat": "mistralai/Mistral-7B-Instruct-v0.1",
        "gemma-7b-instruct": "google/gemma-7b-it",
    }
    PROVIDER_NAME = "Together"
