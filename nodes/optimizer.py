from langchain_core.messages import HumanMessage, SystemMessage
 
from config.llm import optimizer_llm
from state import TweetState
 
_SYSTEM_PROMPT = "You punch up tweets for virality and humor based on given feedback."
 
_USER_TEMPLATE = """
Improve this tweet based on the feedback below.
 
Topic:    "{topic}"
Feedback: "{feedback}"
 
Original tweet:
{tweet}
 
Rewrite it as a short, viral-worthy tweet.
- Avoid Q&A style.
- Stay under 280 characters.
- Keep the same topic angle.
""".strip()
 
 
def optimize_tweet(state: TweetState) -> dict:
    """Rewrite the tweet using the latest evaluator feedback."""
    messages = [
        SystemMessage(content=_SYSTEM_PROMPT),
        HumanMessage(
            content=_USER_TEMPLATE.format(
                topic=state["topic"],
                feedback=state["feedback"],
                tweet=state["tweet"],
            )
        ),
    ]
    tweet = optimizer_llm.invoke(messages).content
    return {
        "tweet": tweet,
        "iteration": state["iteration"] + 1,
        "tweet_history": [tweet],
    }
