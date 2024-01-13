from database.models.metrics import StaticData


static_data = [
    StaticData(
        provider_name="OpenAI",
        url="https://platform.openai.com/docs/api-reference/introduction",
        logo_url="",
        llm_name="gpt-3.5-turbo",
        cost={"in": 1.0, "out": 2.0},
        rate_limit="≤ 10K RPM",
    )
]
