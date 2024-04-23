from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str

    mongo_uri: str

    aws_region: str
    aws_sqs_url: str
    aws_sqs_max_messages: int
    aws_sqs_wait_time_seconds: int

    abacus_api_key: str
    anthropic_api_key: str
    anyscale_api_key: str
    decart_api_key: str
    deepinfra_api_key: str
    fireworks_api_key: str
    lepton_api_key: str
    openai_api_key: str
    perplexity_api_key: str
    replicate_api_token: str
    together_api_key: str

    cache_expiration_in_days: float
    hours_between_collections: int

    class Config:
        files = [".env"]
        if config("ENV") == "dev":
            files.append(".env.dev")
        elif config("ENV") == "prod":
            files.append(".env.prod")

        env_file = files
        env_file_encoding = "utf-8"


settings = Settings()
