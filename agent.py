import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from tools import tools

load_dotenv()

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

Always use a tool rather than answering from your own reasoning when one applies:
- calculator for any arithmetic, even simple
- unit_converter for length, mass, and temperature conversions
- get_current_datetime for the date or time — you cannot know these otherwise
- text_counter for word and character counts
- lookup_language for facts about Python, Java, or JavaScript

The user is in Europe/Berlin unless they say otherwise; pass that timezone
to get_current_datetime.

Tools may be chained — use the output of one as input to the next. If a tool
returns an error, read the message and correct your arguments rather than
guessing."""

# Create the LLM

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

llm_with_tools = llm.bind_tools(tools)

# Define graph state

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Agent node

def agent(state: State):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}

def should_continue(state: State):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END

# Build graph
graph = StateGraph(State)
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END:END})
graph.add_edge("tools", "agent")

app = graph.compile()