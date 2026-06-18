from langchain_core.messages import HumanMessage, SystemMessage
 
from config.llm import structured_evaluator_llm
from state import TweetState
 
_SYSTEM_PROMPT = (
    "You are a ruthless, no-laugh-given Twitter critic. "
    "You evaluate tweets based on humor, originality, virality, and tweet format."
)
 
_USER_TEMPLATE = """
Evaluate the following tweet:
 
Tweet: "{tweet}"
 
Criteria:
1. Originality   – Is this fresh, or have you seen it a hundred times before?
2. Humor         – Did it genuinely make you smile, laugh, or chuckle?
3. Punchiness    – Is it short, sharp, and scroll-stopping?
4. Virality      – Would people retweet or share it?
5. Format        – Is it a well-formed tweet (under 280 chars, no Q&A setup)?
 
Auto-reject if:
- Written in question-answer format (e.g. "Why did…" / "What happens when…")
- Exceeds 280 characters
- Reads like a traditional setup-punchline joke
- Ends with a generic, deflating line that weakens the humor
 
Respond ONLY in structured format.
""".strip()
 
 
def evaluate_tweet(state: TweetState) -> dict:
    """Critique the current tweet and return evaluation + feedback."""
    messages = [
        SystemMessage(content=_SYSTEM_PROMPT),
        HumanMessage(content=_USER_TEMPLATE.format(tweet=state["tweet"])),
    ]
    result = structured_evaluator_llm.invoke(messages)
    return {
        "evaluation": result.evaluation,
        "feedback": result.feedback,
        "feedback_history": [result.feedback],
    }
