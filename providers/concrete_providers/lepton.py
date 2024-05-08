from providers.abstract_providers.base_provider import BaseProvider


class Lepton(BaseProvider):
    ADAPTER_MODEL_STR_MAP = {
        "mixtral-8x7b": "",
        "mixtral-8x22b": "",
        "mistral-7b-chat": "",
        "gemma-7b-instruct": "",
    }
    PROVIDER_NAME = "Lepton"
