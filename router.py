from typing import Literal
 
from state import TweetState
 
 
def route_evaluation(state: TweetState) -> Literal["approved", "needs_improvement"]:
    """
    Return 'approved' when the tweet passes QA *or* we've hit the iteration cap.
    Return 'needs_improvement' to loop back through the optimizer.
    """
    if state["evaluation"] == "approved" or state["iteration"] >= state["max_iteration"]:
        return "approved"
    return "needs_improvement"
