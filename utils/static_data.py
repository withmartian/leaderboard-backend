from database.models.metrics import StaticData


static_data = [
    StaticData(
        provider_name="OpenAI",
        url="https://platform.openai.com/docs/api-reference/introduction",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/OpenAI%20logo.svg",
        cost={
            "gpt-3.5-turbo": {"in": 0.5, "out": 1.5},
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
            "claude-3-haiku": {"in": 0.25, "out": 1.25},
            "claude-3-sonnet": {"in": 3, "out": 15},
            "claude-3-opus": {"in": 15, "out": 75},
        },
        rate_limit="customized",
    ),
    StaticData(
        provider_name="Anyscale",
        url="https://docs.endpoints.anyscale.com/?_gl=1*egjt7v*_ga*MTg2OTk4MjI1MC4xNjk4Mzg3MzA5*_ga_T6EXHYG44V*MTcwNTM1OTQxMi4yNi4xLjE3MDUzNTk0MjIuNTAuMC4xNDU2NDY0ODEz",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Anyscale%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0.5, "out": 0.5},
            "mixtral-8x22b": {"in": 0.9, "out": 0.9},
            "mistral-7b-chat": {"in": 0.15, "out": 0.15},
            "gemma-7b-instruct": {"in": 0.15, "out": 0.15},
            "llama-3-8b-chat": {"in": 0.15, "out": 0.15},
            "llama-3-70b-chat": {"in": 1.0, "out": 1.0},
        },
        rate_limit="30 RPS",
    ),
    StaticData(
        provider_name="DeepInfra",
        url="https://deepinfra.com/docs",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/DeepInfra%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0.24, "out": 0.24},
            "mixtral-8x22b": {"in": 0.65, "out": 0.65},
            "mistral-7b-chat": {"in": 0.07, "out": 0.07},
            "gemma-7b-instruct": {"in": 0.07, "out": 0.07},
            "llama-3-8b-chat": {"in": 0.08, "out": 0.08},
            "llama-3-70b-chat": {"in": 0.59, "out": 0.79},
            "dbrx-instruct": {"in": 0.6, "out": 0.6},
        },
        rate_limit="unlimited",
    ),
    StaticData(
        provider_name="Fireworks",
        url="https://readme.fireworks.ai/docs/quickstart",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Fireworks%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0.5, "out": 0.5},
            "mixtral-8x22b": {"in": 1.2, "out": 1.2},
            "mistral-7b-chat": {"in": 0.2, "out": 0.2},
            "gemma-7b-instruct": {"in": 0.2, "out": 0.2},
            "llama-3-8b-chat": {"in": 0.2, "out": 0.2},
            "llama-3-70b-chat": {"in": 0.9, "out": 0.9},
            "dbrx-instruct": {"in": 1.6, "out": 1.6},
        },
        rate_limit="600 RPM",
    ),
    StaticData(
        provider_name="Lepton",
        url="https://www.lepton.ai/docs/overview/quickstart",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Lepton%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0.5, "out": 0.5},
            "mixtral-8x22b": {"in": 0.8, "out": "?"},
            "mistral-7b-chat": {"in": 0.11, "out": 0.11},
            "gemma-7b-instruct": {"in": 0.1, "out": 0.1},
        },
        rate_limit="10 RPM",
    ),
    StaticData(
        provider_name="Perplexity",
        url="https://docs.perplexity.ai/docs/getting-started",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Perplexity%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0.6, "out": 0.6},
            "mistral-7b-chat": {"in": 0.2, "out": 0.2},
            "llama-3-8b-chat": {"in": 0.2, "out": 0.2},
            "llama-3-70b-chat": {"in": 1.0, "out": 1.0},
        },
        rate_limit="24-100 RPM",
    ),
    StaticData(
        provider_name="Together",
        url="https://docs.together.ai/docs/quickstart",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Together%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0.6, "out": 0.6},
            "mixtral-8x22b": {"in": 1.2, "out": 1.2},
            "mistral-7b-chat": {"in": 0.2, "out": 0.2},
            "gemma-7b-instruct": {"in": 0.2, "out": 0.2},
            "llama-3-8b-chat": {"in": 0.2, "out": 0.2},
            "llama-3-70b-chat": {"in": 0.9, "out": 0.9},
            "dbrx-instruct": {"in": 1.2, "out": 1.2},
        },
        rate_limit="100 RPS",
    ),
    StaticData(
        provider_name="Groq",
        url="https://console.groq.com/docs/quickstart",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/Groq%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0, "out": 0},
            "gemma-7b-instruct": {"in": 0, "out": 0},
            "llama-3-8b-chat": {"in": 0, "out": 0},
            "llama-3-70b-chat": {"in": 0, "out": 0},
        },
        rate_limit="30 RPM",
    ),
    StaticData(
        provider_name="OpenRouter",
        url="https://openrouter.ai/docs#quick-start",
        logo_url="https://provider-leaderboard.sfo3.cdn.digitaloceanspaces.com/OpenRouter%20logo.svg",
        cost={
            "mixtral-8x7b": {"in": 0.24, "out": 0.24},
            "mixtral-8x22b": {"in": 0.65, "out": 0.65},
            "mistral-7b-chat": {"in": 0.1, "out": 0.25},
            "gemma-7b-instruct": {"in": 0.1, "out": 0.1},
            "llama-3-8b-chat": {"in": 0.1, "out": 0.1},
            "llama-3-70b-chat": {"in": 0.81, "out": 0.81},
            "dbrx-instruct": {"in": 0.6, "out": 0.6},
        },
        rate_limit="unlimited",
    ),
]

if __name__ == "__main__":
    from database.models.metrics import update_static_data, save_static_data
    import asyncio

    async def main():
        for data in static_data:
            if data.provider_name in ["Groq"]:
                await update_static_data(data.provider_name, data)

    asyncio.run(main())
    print("done")
