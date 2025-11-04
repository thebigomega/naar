"""Core primitives for tools that can be used by agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ToolFn(Protocol):
    """Protocol that describes the callable signature of a tool."""

    def __call__(self, query: str) -> str:
        """Execute the tool with the provided query string."""


@dataclass(slots=True)
class Tool:
    """A callable utility that an :class:`~naar.agent.Agent` can execute.

    Parameters
    ----------
    name:
        Human readable identifier for the tool.
    description:
        Short summary that helps the agent decide when to execute the tool.
    fn:
        Callable that receives the user query and returns a textual response.
    """

    name: str
    description: str
    fn: ToolFn

    def __call__(self, query: str) -> str:
        """Execute the underlying tool function."""

        return self.fn(query)

