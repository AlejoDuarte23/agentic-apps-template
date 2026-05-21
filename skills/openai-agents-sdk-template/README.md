# OpenAI Agents SDK Template App

This app uses `Agent` and `Runner.run_sync` without setting `model=`, so the Agents SDK uses its default OpenAI model behavior.

## Layout

- `app.py`: CLI entrypoint.
- `agent/runner.py`: agent construction and runner helpers.
- `agent/system_prompt.xml`: XML system prompt.
- `agent/tools/`: function tools grouped by submodule.

## Run

```bash
uv sync
cp .env.example .env
uv run python app.py "Count the words in this sentence and explain the result."
```

Set `OPENAI_API_KEY` before running.
