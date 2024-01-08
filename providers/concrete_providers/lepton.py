from providers.abstract_providers.openai_provider import OpenaiProvider
import openai
import os
from dotenv import load_dotenv

load_dotenv()


class Lepton(OpenaiProvider):
    NAME = "lepton"
    API_KEY = os.environ["LEPTON_API_KEY"]
    SUPPORTED_MODELS = {"llama-2-70b-chat": "llama2-70b"}

    # a mapping of lepton's model alias to their special url
    MODEL_TO_OPENAI_BASE_URL = {
        "llama-2-70b-chat": "https://llama2-70b.lepton.run/api/v1"
    }
    MODEL_TO_HTTP_URL = {
        "llama-2-70b-chat": "https://llama2-70b.lepton.run/api/v1/chat/completions"
    }

    def call_http(
        self,
        model_name: str,
        prompt: str,
        max_tokens: int,
    ) -> float:
        return super().call_http(
            model_name, prompt, max_tokens, self.MODEL_TO_HTTP_URL[model_name]
        )

    def call_sdk(
        self,
        model_name: str,
        prompt: str,
        max_tokens: int,
    ) -> float:
        client = openai.OpenAI(
            base_url=self.MODEL_TO_OPENAI_BASE_URL[model_name], api_key=self.API_KEY
        )
        return super().call_sdk(model_name, prompt, max_tokens, client)

    def get_ttft(self, model_name: str, prompt: str, max_tokens: int = 5) -> float:
        client = openai.OpenAI(
            base_url=self.MODEL_TO_OPENAI_BASE_URL[model_name], api_key=self.API_KEY
        )
        return super().get_ttft(model_name, prompt, max_tokens, client)
