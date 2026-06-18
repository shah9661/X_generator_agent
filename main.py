import argparse
 
from graph import workflow
 
 
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI-powered tweet generator")
    parser.add_argument("--topic", default="Monday mornings", help="Tweet topic")
    parser.add_argument("--max-iter", type=int, default=5, help="Max optimizer loops")
    return parser.parse_args()
 
 
def print_result(result: dict) -> None:
    """Pretty-print the final pipeline output."""
    print("\n" + "═" * 50)
    print(f"  Topic      : {result['topic']}")
    print(f"  Final tweet: {result['tweet']}")
    print(f"  Status     : {result['evaluation']}")
    print(f"  Iterations : {result['iteration']} / {result['max_iteration']}")
    print("─" * 50)
    print(f"  Versions tried ({len(result['tweet_history'])}):")
    for i, t in enumerate(result["tweet_history"], 1):
        print(f"    [{i}] {t}")
    print("═" * 50 + "\n")
 
 
def run(topic: str, max_iteration: int = 5) -> dict:
    """Invoke the workflow and return the final state."""
    initial_state = {
        "topic": topic,
        "iteration": 0,          
        "max_iteration": max_iteration,  
    }
    return workflow.invoke(initial_state)
 
 
if __name__ == "__main__":
    args = parse_args()
    result = run(topic=args.topic, max_iteration=args.max_iter)
    print_result(result)
