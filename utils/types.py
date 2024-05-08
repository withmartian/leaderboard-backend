from enum import Enum


class ModelName(str, Enum):
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    GPT3_TURBO = "gpt-3.5-turbo"
    CLAUDE3_HAIKU = "claude-3-haiku"
    CLAUDE3_SONNET = "claude-3-sonnet"
    CLAUDE3_OPUS = "claude-3-opus"
    DBRX = "dbrx-instruct"
    LLAMA3_8B = "llama-3-8b-chat"
    LLAMA8_70B = "llama-3-70b-chat"
    MIXTRAL_8X7B = "mixtral-8x7b"
    MIXTRAL_8X22B = "mixtral-8x22b"
    MISTRAL_7B = "mistral-7b-chat"
    GEMMA_7B = "gemma-7b-instruct"


class TokenCounts(int, Enum):
    THOUSAND = 1000
    HUNDRED = 100
