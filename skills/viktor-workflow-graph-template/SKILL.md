---
name: viktor-workflow-graph-template
description: Create a VIKTOR app template with OpenAI Agents SDK chat, an agent/runner.py module, agent/system_prompt.xml, grouped agent tools, workflow graph rendering, streamed tool-call status in chat, VIKTOR SDK API helpers, and vkt.Storage handoffs between tools.
---

# VIKTOR Workflow Graph Template

Use this skill when building a VIKTOR app that combines an agent chat, a workflow graph WebView, tool-call progress in chat, remote VIKTOR app calls, and entity-scoped `vkt.Storage` handoffs.

## Grounding

This template follows the local VIKTOR skill sequence:

1. Load `viktor-core` for `app.py`, `Parametrization`, `Controller`, views, and `vkt.UserError`.
2. Load `viktor-parametrization` before changing inputs.
3. Load `viktor-styling` before writing app text.
4. Load `viktor-cli-config` before creating or running the app.
5. Load `viktor-sdk-api` for `vkt.api_v1.API` entity navigation and compute calls.
6. Load `viktor-rest-api` only if the SDK API cannot cover the required operation.

It also mirrors the inspected repository patterns:

- `app/workflow_graph/models.py`, `state.py`, and `viewer.py` for schema, storage state, and self-contained HTML.
- `app/agent/tools/graph_tools/` for workflow graph composition, plan updates, and progress tools.
- `app/agent/tools/viktor_tools/` for storage tools and remote VIKTOR app tools.
- `app/agent/runner.py` for `Runner.run_streamed(...)` into `vkt.ChatResult`, including rendered tool-call rows.
- `app/agent/system_prompt.xml` for XML-structured agent instructions.
- `app/viktor_tools/base.py` for SDK `Entity.compute(...)` calls against remote views or buttons.
- Footing and pile tools for storage handoff: producer writes JSON with `vkt.Storage().set(...)`, consumer reads with `getvalue_binary().decode("utf-8")`.

## Template Location

This folder is the VIKTOR app template root. Copy the app files from this folder into a new VIKTOR app folder.

## Required Environment

- `OPENAI_API_KEY` for the OpenAI Agents SDK.
- `TOKEN_VK_APP` or `VIKTOR_TOKEN` for cross-workspace SDK API calls.
- `VIKTOR_ENVIRONMENT`, for example `cloud.us1.viktor.ai`, only when using the SDK API from an external script.

## First Run

```bash
viktor-cli create-app "Workflow Graph Agent" --registered-name workflow-graph-agent
viktor-cli clean-start
```

Make sure `viktor.config.toml` contains the same `registered_name`.

## Implementation Rules

1. Keep `app.py` as the VIKTOR entrypoint.
2. Keep workflow graph schema and state in `workflow_graph/`.
3. Keep agent and runner code in `agent/runner.py`.
4. Keep the system prompt in `agent/system_prompt.xml`.
5. Keep graph tools in `agent/tools/graph_tools/`, VIKTOR-facing tools in `agent/tools/viktor_tools/`, and low-level VIKTOR SDK helpers in top-level `viktor_tools/`.
6. Always call `compose_workflow_graph` before plan or progress tools.
7. Always call `get_workflow_plan` before `update_workflow_plan`.
8. Store intermediate JSON under stable entity-scoped keys with `vkt.Storage`.
9. Prefer `vkt.api_v1.API()` inside VIKTOR Python code when it can run the needed computation.
10. Prefer `Entity.compute(method_name="get_data_view", params=...)` for DataView outputs and store `result["data"]` in `vkt.Storage`.
11. Use REST jobs only as a fallback for operations not exposed by SDK compute.
12. Stream tool calls into chat by consuming `result.stream_events()` and rendering `tool_called` and `tool_output` events.

## Files

- `app.py`: VIKTOR controller and graph WebView.
- `agent/runner.py`: OpenAI Agents SDK agent construction and streamed runner.
- `agent/system_prompt.xml`: XML system prompt.
- `agent/tools/graph_tools/`: graph, plan, and progress tools.
- `agent/tools/viktor_tools/`: storage and remote app tools.
- `workflow_graph/`: graph models, state, renderer, CSS, and JS.
- `viktor_tools/`: SDK compute client, SDK API examples, and storage helpers.
- `requirements.txt`: Python dependencies for the VIKTOR app.
- `viktor.config.toml`: local VIKTOR app config.
