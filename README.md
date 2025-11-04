# Naar

A tiny example of an autonomous agent that can register tools, choose one based on
keyword matching, and keep a reasoning trace. The default configuration includes
simple "calculator" and "summarize" tools.

## Usage

```bash
python -m naar.cli "2 + 2"
# -> 4
```

The agent attempts to pick the best tool for the given prompt. When a tool
returns a response prefixed with ``done:``, the agent treats the remaining text
as the final answer.

To inspect the reasoning trace:

```python
from naar.cli import make_default_agent

agent = make_default_agent()
agent.run("Write a short summary of agents")
print(agent.explain())
```

