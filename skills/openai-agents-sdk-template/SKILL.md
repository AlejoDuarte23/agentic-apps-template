---
name: openai-agents-sdk-template
description: Create a minimal Python OpenAI Agents SDK app that uses the SDK default OpenAI LLM out of the box. Use when scaffolding a small runnable agent with optional function tools, no explicit model setting, and a simple CLI smoke test.
---

# OpenAI Agents SDK Template

Use this skill to create a small Python app with the OpenAI Agents SDK and the default OpenAI model provider.

## Sources To Keep In Mind

- Official Agents SDK docs: `https://openai.github.io/openai-agents-python/`
- Agent Skills structure: `https://agentskills.io/specification`

## Template Location

This folder is the app template root. Copy the app files from this folder into the target project.

The template intentionally does not pass `model=` to `Agent` or `RunConfig`. That lets the SDK use its out-of-the-box OpenAI model behavior. If the project needs one default model for every agent, set `OPENAI_DEFAULT_MODEL` in the environment instead of hardcoding a model in the template.

## Workflow

1. Copy this app template folder to the new app folder.
2. Set `OPENAI_API_KEY` in the shell or `.env`.
3. Install dependencies with the project package manager. For this template:

   ```bash
   uv sync
   ```

4. Run a smoke test:

   ```bash
   uv run python app.py "Summarize the responsibilities of this template."
   ```

5. Add only deterministic, narrow tools under `agent/tools/`. Keep side effects explicit and easy to audit.

## Files

- `app.py`: CLI entrypoint.
- `agent/runner.py`: agent factory and one-shot runner.
- `agent/system_prompt.xml`: XML system prompt.
- `agent/tools/`: example `@function_tool` functions grouped by submodule.
- `pyproject.toml`: minimal dependency metadata.
- `.env.example`: required environment variables.
- `TEMPLATE.md`: code-only pasteable version.
