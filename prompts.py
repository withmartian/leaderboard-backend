# This is 100 and 1000 tokens for Llama, but 93 and 943 tokens for mixtral.
# The marginal error shouldn't create a big difference, so we are using the same prompt for both models for now

PROMPT_100_TOKENS = "Tell me a long story based on the following story description: In a future world where emotions are regulated by technology, a girl discovers a hidden garden that awakens real feelings. She embarks on a journey to understand these new emotions, challenging the societal norms and the oppressive tech that controls them. Alongside a group of outcasts, she fights to bring authentic emotions back to a world that has forgotten how to feel."


def get_prompt() -> str:
    return PROMPT_100_TOKENS
