from providers.abstract_providers.openai_provider import OpenaiProvider
import openai
import os
from dotenv import load_dotenv
import httpx

load_dotenv()


class Lepton(OpenaiProvider):
    NAME = "Lepton"
    API_KEY = os.environ["LEPTON_API_KEY"]
    SUPPORTED_MODELS = {"llama2-70b-chat": "llama2-70b", "mixtral-8x7b": "mixtral-8x7b"}

    # a mapping of lepton's model alias to their special url
    MODEL_TO_OPENAI_BASE_URL = {
        "llama2-70b-chat": "https://llama2-70b.lepton.run/api/v1",
        "mixtral-8x7b": "https://mixtral-8x7b.lepton.run/api/v1/",
    }

    async def call_sdk(
        self,
        llm_name: str,
        prompt: str,
        max_tokens: int,
    ) -> float:
        client = openai.AsyncOpenAI(
            base_url=self.MODEL_TO_OPENAI_BASE_URL[llm_name],
            api_key=self.API_KEY,
            http_client=httpx.AsyncClient(http2=True),
        )
        return await super().call_sdk(llm_name, prompt, max_tokens, client)

    async def call_streaming(
        self, llm_name: str, prompt: str, max_tokens: int = 5
    ) -> float:
        client = openai.AsyncOpenAI(
            base_url=self.MODEL_TO_OPENAI_BASE_URL[llm_name],
            api_key=self.API_KEY,
            http_client=httpx.AsyncClient(http2=True),
        )
        return await super().call_streaming(llm_name, prompt, max_tokens, client)
