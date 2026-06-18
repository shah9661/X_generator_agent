from langgraph.graph import END, START, StateGraph
 
from nodes.evaluator import evaluate_tweet
from nodes.generator import generate_tweet
from nodes.optimizer import optimize_tweet
from router import route_evaluation
from state import TweetState
 
 
def build_graph() -> StateGraph:
    """Wire up nodes, edges, and conditional routing."""
    graph = StateGraph(TweetState)
 
    graph.add_node("generate", generate_tweet)
    graph.add_node("evaluate", evaluate_tweet)
    graph.add_node("optimize", optimize_tweet)
 
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "evaluate")
    graph.add_conditional_edges(
        "evaluate",
        route_evaluation,
        {"approved": END, "needs_improvement": "optimize"},
    )
    graph.add_edge("optimize", "evaluate")
 
    return graph
 
 

workflow = build_graph().compile()
