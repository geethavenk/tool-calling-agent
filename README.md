# Tool-Calling Agent

A simple tool-calling AI agent built with Python, LangChain, and LangGraph.

The agent uses five tools:

- Calculator
- Unit converter
- Date/time
- Text counter
- Language lookup

## Setup

Install the required packages:

```bash
pip install -r requirements.txt
```

Create the `.env` file from the example:

```bash
cp .env.example .env
```

Then add your API keys to the `.env` file.

Start the application:

```bash
python main.py
```

## LangSmith Tracing

This project uses LangSmith to trace and monitor the agent workflow.

Add the following to your `.env` file:

```text
LANGSMITH_TRACING=true
LANGSMITH_API_KEY="your_langsmith_api_key"
LANGSMITH_PROJECT=tool-calling-agent
```

Run the application:

```bash
python main.py
```

Then try a sample query:

```text
Calculate 18% GST on 74500.
```

The agent should select and execute the `calculator` tool.

The execution trace can be viewed in the `tool-calling-agent` project in LangSmith.

## Structure

- `tools.py` — tool definitions
- `agent.py` — LangGraph agent workflow
- `main.py` — interactive CLI