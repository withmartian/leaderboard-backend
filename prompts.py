# This is 100 and 1000 tokens for Llama, but 93 and 943 tokens for mixtral.
# The marginal error shouldn't create a big difference, so we are using the same prompt for both models for now

PROMPT_100_TOKENS = "Tell me a long story based on the following story description: In a future world where emotions are regulated by technology, a girl discovers a hidden garden that awakens real feelings. She embarks on a journey to understand these new emotions, challenging the societal norms and the oppressive tech that controls them. Alongside a group of outcasts, she fights to bring authentic emotions back to a world that has forgotten how to feel."
PROMPT_1000_TOKENS = """In the year 2124, the world was a place of perfect order, where emotions were meticulously regulated by the ubiquitous EmoTech devices. These small, sleek implants, embedded at the base of every citizen's skull, controlled the human emotional spectrum, ensuring productivity and suppressing any feeling deemed unproductive or dangerous. In this world lived Ava, a young woman with chestnut hair and inquisitive eyes, who worked as a botanist in the city's central bio-dome.

Ava's life was a sequence of measured routines until one day, during a routine soil analysis in the outskirts of the city, she stumbled upon a hidden garden. This place, untouched by the cold hands of technology, was a riot of colors and fragrances, a stark contrast to the sterile grays of the city. As she stepped into this secret haven, her EmoTech glitched for a moment, and a rush of unfiltered emotions flooded her senses.

This garden became Ava's escape. She would sneak away to it, feeling her heart swell with emotions that were both terrifying and exhilarating. In the garden, she met others like her, outcasts who had discovered this place and, with it, their true selves. They were a diverse group: Leo, a former engineer with a gentle soul; Mira, a fiery artist who painted the garden's beauty; and Jin, a quiet philosopher who questioned the world's reliance on EmoTech.

Together, they shared stories, laughed, and cried, experiencing the spectrum of emotions that had been stolen from them. Ava felt a bond with these strangers that she had never known before. They became her family, united by the desire to feel, to live authentically.

Ava's growing discontent with the emotionless world outside the garden led her to delve into the history of EmoTech. She learned that it was introduced by the government as a solution to the chaotic world plagued by emotional crimes, mental illness, and unproductive behaviors. Society had embraced it as a panacea, trading their emotional freedom for security and efficiency.

The group decided that it was time for change. They started by creating art, music, and literature filled with real emotions and secretly distributing them among the population. These works sparked curiosity and confusion, as people experienced flickers of emotions they couldn't understand.

Their movement grew as more people began to question the world around them. The government, noticing the shift, tightened its control, but the desire for authentic emotions was like a fire that couldn't be extinguished. Ava and her friends organized gatherings, where they would temporarily disable their EmoTech and let people experience real emotions. These gatherings were risky, but the hunger for genuine feeling was powerful.

As their revolution gained momentum, Ava and her friends faced increasing dangers. They were pursued by the authorities, labeled as emotion terrorists, and faced the threat of being disconnected from society, a fate considered worse than death. But their determination only grew stronger.

In a final act of defiance, Ava and her team infiltrated the main EmoTech control center. They intended to broadcast a signal that would disable the EmoTech devices, even for a brief moment, giving everyone a taste of true emotion.

The mission was fraught with challenges, but their resolve was unbreakable. As they reached the control room, they were confronted by the authorities. A tense standoff ensued, with Ava and her friends surrounded. In those desperate moments, Ava delivered a passionate speech about the beauty of emotions, the joy, the pain, and the depth they added to life. Her words, broadcasted accidentally over the city's communication system, touched the hearts of many.

In a surprising turn of events, the officers, moved by Ava's words, allowed them to send the broadcast. The signal was sent, and for a brief moment, the city was awash with pure, unregulated emotion. People cried, laughed, and embraced, overwhelmed by the intensity of their feelings.

Now, continue writing Ava's story. Be creative about what happens next, and make sure to tell a long story
"""

TOKEN_COUNTS_TO_PROMPT = {100: PROMPT_1000_TOKENS, 1000: PROMPT_1000_TOKENS}


def get_prompt(input_tokens: int) -> str:
    return TOKEN_COUNTS_TO_PROMPT[input_tokens]
