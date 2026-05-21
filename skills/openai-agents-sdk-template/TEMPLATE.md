# Code Template

```python
from pathlib import Path

from agents import Agent, Runner

from agent.tools import count_words


def build_agent() -> Agent:
    prompt = (Path(__file__).parent / "agent" / "system_prompt.xml").read_text()
    return Agent(name="Template Assistant", instructions=prompt, tools=[count_words])


def run_once(user_input: str) -> str:
    result = Runner.run_sync(build_agent(), user_input)
    return str(result.final_output)
```

```python
from agents import function_tool


@function_tool
def count_words(text: str) -> dict[str, int]:
    words = [word for word in text.split() if word.strip()]
    return {"characters": len(text), "words": len(words)}
```
