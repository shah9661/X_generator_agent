from langchain_core.messages import HumanMessage, SystemMessage
 
from config.llm import generator_llm
from state import TweetState
 
_SYSTEM_PROMPT = "You are a funny and clever Twitter/X influencer."
 
_USER_TEMPLATE = """
Write a short, original, and hilarious tweet on the topic: "{topic}".
 
Rules:
- Do NOT use question-answer format.
- Max 280 characters.
- Use observational humor, irony, sarcasm, or cultural references.
- Think in meme logic, punchlines, or relatable takes.
- Use simple, everyday English.
""".strip()
 
 
def generate_tweet(state: TweetState) -> dict:
    """Generate a fresh tweet based on the topic."""
    messages = [
        SystemMessage(content=_SYSTEM_PROMPT),
        HumanMessage(content=_USER_TEMPLATE.format(topic=state["topic"])),
    ]
    tweet = generator_llm.invoke(messages).content
    return {
        "tweet": tweet,
        "tweet_history": [tweet],
    }
