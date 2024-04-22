from enum import Enum


class ModelName(str, Enum):
    LLAMA2_70B_CHAT = "llama2-70b-chat"
    MIXTRAL_8X7B = "mixtral-8x7b"
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    GPT3_TURBO = "gpt-3.5-turbo"
    CLAUDE2 = "claude-2.1"
    CLAUDE_INSTANT = "claude-instant-1.2"


class TokenCounts(int, Enum):
    THOUSAND = 1000
    HUNDRED = 100
