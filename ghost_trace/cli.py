import cyclopts
from rich.console import Console
from rich.table import Table
from ghost_trace.tracer import GhostTracer

app = cyclopts.App(help="Ghost Trace: Professional observability for your AI agent.")
console = Console()

@app.command
def view(limit: int = 20, db: str = "ghost_trace.db"):
    """View the latest agent execution traces."""
    tracer = GhostTracer(db)
    traces = tracer.get_traces(limit)
    
    if not traces:
        console.print("[yellow]No traces found. Wrap your agent tools with GhostTracer.trace() first.[/yellow]")
        return

    table = Table(title="Ghost Agent Traces")
    table.add_column("Status", style="bold")
    table.add_column("Tool", style="cyan")
    table.add_column("Arguments", style="magenta")
    table.add_column("Result", style="green")
    table.add_column("Time (s)", justify="right")

    for t in traces:
        status = "[red]ERROR[/red]" if t["error"] else "[green]OK[/green]"
        # Truncate long strings for the table
        args = (t["arguments"][:40] + "...") if len(t["arguments"]) > 40 else t["arguments"]
        result = (t["result"][:40] + "...") if t["result"] and len(t["result"]) > 40 else (t["result"] or "")
        
        table.add_row(status, t["tool_name"], args, result, f"{t['duration']:.2f}")

    console.print(table)

if __name__ == "__main__":
    app()
