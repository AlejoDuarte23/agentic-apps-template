from pathlib import Path

from agents import Agent, Runner

from agent.tools import count_words


PROMPT_PATH = Path(__file__).resolve().parent / "system_prompt.xml"


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_agent() -> Agent:
    return Agent(
        name="Template Assistant",
        instructions=load_system_prompt(),
        tools=[count_words],
    )


def run_once(user_input: str) -> str:
    result = Runner.run_sync(build_agent(), user_input)
    return str(result.final_output)
