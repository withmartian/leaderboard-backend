from abc import ABC, abstractmethod


class AbstractProvider(ABC):
    PROVIDER_NAME = None

    @abstractmethod
    def call_http(self, model_name: str, prompt: str, max_tokens: int) -> int:
        """
        Calls the provider endpoint through http requests and return the number of output tokens
        """
        pass

    @abstractmethod
    def call_sdk(self, model_name: str, prompt: str, max_tokens: int) -> int:
        """
        Calls the provider endpoint through openai client python package if available, else the provider's own python SDK.
        Return the number of output tokens
        """
        pass

    @abstractmethod
    def get_ttft(self, model_name: str, prompt: str, max_tokens: int) -> float:
        """
        Returns the time to first token (TTFT) in seconds via the openai client python package using streaming.
        If the provider doesn't support the openai client python package, use its SDK.
        Return the TTFT in seconds
        """
        pass
