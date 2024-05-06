from providers.abstract_providers.base_provider import BaseProvider


class Openai(BaseProvider):
    ADAPTER_MODEL_STR_MAP = {
        "gpt-4-turbo": "gpt-4-turbo",
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        "gpt-4": "gpt-4",
    }
    PROVIDER_NAME = "OpenAI"
