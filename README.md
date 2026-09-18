# Tool-Calling Agent

A LangGraph ReAct agent with five tools: calculator, unit converter,
datetime, text counter, and language lookup.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env    # then fill in your key
python main.py
```

## Structure

- `tools.py` — tool definitions
- `agent.py` — graph construction
- `main.py` — interactive CLI