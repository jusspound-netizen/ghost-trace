from ghost_trace.tracer import GhostTracer
import time

tracer = GhostTracer()

@tracer.trace
def get_weather(city: str):
    """Simulate a tool call."""
    time.sleep(0.5)
    return f"Sunny in {city}"

@tracer.trace
def fail_tool():
    raise ValueError("Simulated API failure")

# Run them
get_weather(city="London")
try:
    fail_tool()
except:
    pass

print("Traces written to ghost_trace.db")
