# Ghost Trace

Professional observability for your AI agent.

Ghost Trace is a lightweight, local-first CLI that intercepts your agent's tool calls and logs them to a SQLite database. No cloud accounts, no API keys, no heavy infrastructure. Just a beautiful trace of what your agent is doing.

## Why use it?

Debugging AI agents with print() statements is painful. When an agent fails on step 4 of a 10-step task, you need to know exactly which tool failed, what arguments it received, and how long it took.

Ghost Trace gives you a clean, color-coded table of every tool call.

## Installation

pip install ghost-tracer

## Usage

1. Wrap your tools:

from ghost_trace.tracer import GhostTracer
tracer = GhostTracer()

@tracer.trace
def get_weather(city: str):
    return f"Sunny in {city}"

2. View the trace:

ghost-trace view

This will print a table of all recent tool calls, including errors and execution times.

## License

MIT
