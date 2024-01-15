from abc import ABC, abstractmethod
from typing import Callable


class BaseProvider(ABC):
    SUPPORTED_MODELS = {}
    RATE_LIMIT_EXCLUDED_PAIRS = []

    @abstractmethod
    async def call_http(
        self,
        llm_name: str,
        prompt: str,
        max_tokens: int,
        url: str = None,
        get_completion_tokens: Callable = None,
    ) -> int:
        """
        Calls the provider endpoint through http requests and return the tokens/s of the call
        """
        pass

    @abstractmethod
    def call_sdk(self, llm_name: str, prompt: str, max_tokens: int) -> int:
        """
        Calls the provider endpoint through openai client python package if available, else the provider's own python SDK.
        Return the tokens/s of the call
        """
        pass

    @abstractmethod
    async def call_streaming(
        self, llm_name: str, prompt: str, max_tokens: int
    ) -> float:
        """
        Returns the time to first token (TTFT) in seconds via the openai client python package using streaming.
        If the provider doesn't support the openai client python package, use its SDK.
        Return the TTFT in seconds
        """
        pass

    def get_supported_models(self):
        return list(self.SUPPORTED_MODELS.keys())

    def get_rate_limit_excluded_pairs(self):
        return self.RATE_LIMIT_EXCLUDED_PAIRS
