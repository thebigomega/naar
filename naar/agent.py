"""A simple, self-contained agent implementation."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, Iterable, List, Optional

from .tool import Tool


@dataclass
class AgentStep:
    """A single reasoning step taken by the agent."""

    tool: Optional[str]
    prompt: str
    response: str


class Agent:
    """Light-weight agent that can execute tools and keep a trace of its work."""

    def __init__(self, name: str, instructions: str, *, default_response: str | None = None) -> None:
        self.name = name
        self.instructions = instructions.strip()
        self.default_response = default_response or "I do not have enough information to answer that."
        self._tools: Dict[str, Tool] = {}
        self._history: List[AgentStep] = []

    @property
    def tools(self) -> Dict[str, Tool]:
        """Return the registered tools (read-only)."""

        return dict(self._tools)

    @property
    def history(self) -> Iterable[AgentStep]:
        """Return the reasoning steps taken so far."""

        return tuple(self._history)

    def register_tool(self, tool: Tool) -> None:
        """Register a tool that the agent can execute."""

        if tool.name in self._tools:
            raise ValueError(f"A tool named '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def _select_tool(self, task: str) -> Optional[Tool]:
        """Return the tool whose description best matches the task."""

        if not self._tools:
            return None

        task_keywords = set(re.findall(r"[a-zA-Z0-9_]+", task.lower()))
        text_hints = {"text", "summary", "summarize", "summarise", "explain", "describe", "paraphrase"}
        math_hints = {"math", "arithmetic", "number", "numbers", "calculate", "calculation"}
        best_score = -1
        best_tool: Optional[Tool] = None
        for tool in self._tools.values():
            description_keywords = set(re.findall(r"[a-zA-Z0-9_]+", tool.description.lower()))
            score = len(task_keywords & description_keywords)
            if text_hints & task_keywords and text_hints & description_keywords:
                score += 1
            if (any(ch.isdigit() for ch in task) or any(ch in "+-*/" for ch in task)) and math_hints & description_keywords:
                score += 1
            if score > best_score:
                best_score = score
                best_tool = tool

        return best_tool

    def run(self, task: str, *, max_turns: int = 3) -> str:
        """Execute the agent on a task and return the final response."""

        task = task.strip()
        if not task:
            raise ValueError("Task cannot be empty.")

        observation = task
        final_response: Optional[str] = None

        for _ in range(max_turns):
            tool = self._select_tool(observation)
            if tool is None:
                break

            response = tool(observation)
            self._history.append(AgentStep(tool=tool.name, prompt=observation, response=response))
            final_response = response
            observation = response

            if response.strip().lower().startswith("done:"):
                final_response = response.split(":", 1)[1].strip()
                break

        if final_response is None:
            final_response = self.default_response
            self._history.append(AgentStep(tool=None, prompt=task, response=final_response))

        return final_response

    def explain(self) -> str:
        """Return a human readable summary of the reasoning trace."""

        if not self._history:
            return f"{self.name} has not performed any actions yet."

        lines = [f"Agent: {self.name}", f"Instructions: {self.instructions}", "Trace:"]
        for idx, step in enumerate(self._history, 1):
            tool_name = step.tool or "(none)"
            lines.append(f"  {idx}. tool={tool_name} prompt={step.prompt!r} -> {step.response!r}")
        return "\n".join(lines)

