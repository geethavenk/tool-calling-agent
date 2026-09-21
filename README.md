# Tool-Calling Agent

A simple tool-calling AI agent built with Python, LangChain, and LangGraph.

The agent uses five tools:
- Calculator
- Unit converter
- Date/time
- Text counter
- Language lookup

## Setup

```bash
pip install -r requirements.txt

cp .env.example .env    # then add your API keys

python main.py

## LangSmith Tracing

This project uses LangSmith to trace and monitor the agent workflow.

Add the following to your `.env` file:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY="your_langsmith_api_key"
LANGSMITH_PROJECT=tool-calling-agent