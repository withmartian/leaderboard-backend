from database.models.metrics import StaticData


static_data = [
    StaticData(
        provider_name="OpenAI",
        url="https://platform.openai.com/docs/api-reference/introduction",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/OpenAI%20logo.svg",
        cost={
            "gpt-3.5-turbo": {"in": 1.0, "out": 2.0},
            "gpt-4-turbo": {"in": 10.0, "out": 30.0},
            "gpt-4": {"in": 30.0, "out": 60.0},
        },
        rate_limit="10K RPM",
    ),
    StaticData(
        provider_name="Anthropic",
        url="https://docs.anthropic.com/claude/reference/getting-started-with-the-api",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Anthropic%20logo.svg",
        cost={
            "claude-2.1": {"in": 8.0, "out": 24.0},
            "claude-instant-1.2": {"in": 0.8, "out": 2.4},
        },
        rate_limit="customized",
    ),
    StaticData(
        provider_name="Anyscale",
        url="https://docs.endpoints.anyscale.com/?_gl=1*egjt7v*_ga*MTg2OTk4MjI1MC4xNjk4Mzg3MzA5*_ga_T6EXHYG44V*MTcwNTM1OTQxMi4yNi4xLjE3MDUzNTk0MjIuNTAuMC4xNDU2NDY0ODEz",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Anyscale%20logo.svg",
        cost={
            "llama2-70b-chat": {"in": 1.0, "out": 1.0},
            "mixtral-8x7b": {"in": 0.5, "out": 0.5},
        },
        rate_limit="30 RPS",
    ),
    StaticData(
        provider_name="Decart",
        url="https://dashboard.decart.ai/",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Decart%20logo.svg",
        cost={"llama2-70b-chat": {"in": 0.5, "out": 0.5}},
        rate_limit="1M TPM",
    ),
    StaticData(
        provider_name="DeepInfra",
        url="https://deepinfra.com/docs",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/DeepInfra%20logo.svg",
        cost={
            "llama2-70b-chat": {"in": 0.7, "out": 0.9},
            "mixtral-8x7b": {"in": 0.27, "out": 0.27},
        },
        rate_limit="unlimited",
    ),
    StaticData(
        provider_name="Fireworks",
        url="https://readme.fireworks.ai/docs/quickstart",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Fireworks%20logo.svg",
        cost={
            "llama2-70b-chat": {"in": 0.9, "out": 0.9},
            "mixtral-8x7b": {"in": 0.5, "out": 0.5},
        },
        rate_limit="100 RPM",
    ),
    StaticData(
        provider_name="Lepton",
        url="https://www.lepton.ai/docs/overview/quickstart",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Lepton%20logo.svg",
        cost={
            "llama2-70b-chat": {"in": 0.8, "out": 0.8},
        },
        rate_limit="10 RPM",
    ),
    StaticData(
        provider_name="Perplexity",
        url="https://docs.perplexity.ai/docs/getting-started",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Perplexity%20logo.svg",
        cost={
            "llama2-70b-chat": {"in": 1.0, "out": 1.0},
            "mixtral-8x7b": {"in": 0.6, "out": 0.6},
        },
        rate_limit="12 RPM",
    ),
    StaticData(
        provider_name="Replicate",
        url="https://replicate.com/docs/get-started/python",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Replicate%20logo.svg",
        cost={
            "llama2-70b-chat": {"in": 0.65, "out": 2.75},
            "mixtral-8x7b": {"in": 0.3, "out": 1.0},
        },
        rate_limit="10 RPS",
    ),
    StaticData(
        provider_name="Together",
        url="https://docs.together.ai/docs/quickstart",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Together%20logo.svg",
        cost={
            "llama2-70b-chat": {"in": 0.9, "out": 0.9},
            "mixtral-8x7b": {"in": 0.6, "out": 0.6},
        },
        rate_limit="100 RPS",
    ),
    StaticData(
        provider_name="Abacus",
        url="https://abacus.ai/app/llmapis/playground",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Abacus%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0.3, "out": 1},
        },
        rate_limit="unknown",
    ),
]

if __name__ == "__main__":
    from database.models.metrics import save_static_data
    import asyncio

    async def main():
        for data in static_data:
            await save_static_data(data)

    asyncio.run(main())
