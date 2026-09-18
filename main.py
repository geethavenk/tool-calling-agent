from langchain_core.messages import HumanMessage
from agent import app

def run_agent(query, verbose=False):
    """
    Run one query through the agent.

    Returns (final_answer, tool_names_used). With verbose=True, also prints
    the full message trace.
    """
    result = app.invoke({"messages": [HumanMessage(content=query)]})

    used = [
        call["name"]
        for msg in result["messages"]
        for call in getattr(msg, "tool_calls", None) or []
    ]

    if verbose:
        print("\n--- TRACE ---")
        for msg in result["messages"]:
            msg.pretty_print()

    return result["messages"][-1].content, used

QUERIES = [
    # Arithmetic — should hit calculator, not mental math
    "Calculate 18% GST on 74500.",
    "What will 50000 become after adding 12%?",

    # Conversion
    "Convert 15 kilometers into miles.",
    "Is 30 degrees celsius warmer than 90 fahrenheit?",

    # Date/time — checks the Europe/Berlin timezone lands
    "Tell me today's date.",

    # Text
    "How many words are in the sentence: LangGraph makes it easier to build AI agents.",

    # Lookup
    "Tell me about Python.",

    # Chaining — text_counter then calculator
    "How many words are in 'LangGraph makes it easier to build AI agents' "
    "and how many more would I need to reach 20?",

    # No tool applies — checks the model doesn't force a call
    "What is an AI agent?",
]

def main():
    print("Type 'quit' to exit, 'verbose' to toggle the trace.\n")
    verbose = False

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query:
            continue
        if query.lower() in {"quit", "exit"}:
            break
        if query.lower() == "verbose":
            verbose = not verbose
            print(f"Verbose {'on' if verbose else 'off'}.")
            continue

        try:
            response, used = run_agent(query, verbose=verbose)
            print(f"[tools: {', '.join(used) if used else 'none'}]")
            print(f"Assistant: {response}\n")
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}\n")

    print("Bye.")

if __name__ == "__main__":
    main()