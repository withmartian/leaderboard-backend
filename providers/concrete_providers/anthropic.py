from providers.abstract_providers.base_provider import BaseProvider


class Anthropic(BaseProvider):
    ADAPTER_MODEL_STR_MAP = {
        "claude-3-sonnet": "claude-3-sonnet-20240229",
        "claude-3-opus": "claude-3-opus-20240229",
        "claude-3-haiku": "claude-3-haiku-20240307",
    }
    PROVIDER_NAME = "Anthropic"
