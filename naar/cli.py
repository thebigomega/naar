"""Command line interface for interacting with the example agent."""

from __future__ import annotations

import argparse
from .agent import Agent
from .tool import Tool


def make_default_agent() -> Agent:
    """Create an agent with two demonstration tools."""

    agent = Agent(
        name="Naar",
        instructions=(
            "Use the calculator when numbers are involved. "
            "Otherwise, echo back what the user said as a reflective summary."
        ),
    )

    def calculator(query: str) -> str:
        try:
            result = eval(query, {"__builtins__": {}}, {})  # noqa: S307 - safe globals
        except Exception as exc:  # pragma: no cover - defensive branch
            return f"Could not evaluate expression: {exc}"
        return f"done: {result}"

    def summarize(query: str) -> str:
        return f"done: You asked me to think about '{query}'."

    agent.register_tool(Tool(name="calculator", description="math arithmetic numbers", fn=calculator))
    agent.register_tool(Tool(name="summarize", description="text summary paraphrase", fn=summarize))
    return agent


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Interact with the Naar example agent.")
    parser.add_argument("prompt", help="Task you would like the agent to attempt.")
    parsed = parser.parse_args(args=args)

    agent = make_default_agent()
    result = agent.run(parsed.prompt)
    print(result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

