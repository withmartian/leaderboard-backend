from abc import ABC, abstractmethod
from typing import Callable


class BaseProvider(ABC):
    NAME = None

    @abstractmethod
    def call_http(
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
    def get_ttft(self, llm_name: str, prompt: str, max_tokens: int) -> float:
        """
        Returns the time to first token (TTFT) in seconds via the openai client python package using streaming.
        If the provider doesn't support the openai client python package, use its SDK.
        Return the TTFT in seconds
        """
        pass

    def get_request_method(self, request_method: str) -> Callable:
        if request_method == "http":
            return self.call_http
        elif request_method == "sdk":
            return self.call_sdk
