# VIKTOR Workflow Graph Agent Template

This template combines:

- `vkt.Chat` backed by the OpenAI Agents SDK.
- A `@vkt.WebView` workflow graph that reads `WorkflowCanvasState` from `vkt.Storage`.
- Function tools for composing a DAG, updating plan items, and rendering progress.
- Chat rows for tool calls by streaming `tool_called` and `tool_output` events.
- SDK API helpers for calling another VIKTOR app through `vkt.api_v1.Entity.compute`.
- Entity-scoped storage helpers for passing output from one tool to another.

## Layout

- `app.py`: VIKTOR controller and views.
- `agent/runner.py`: OpenAI Agents SDK agent, runner, and stream handling.
- `agent/system_prompt.xml`: XML system prompt.
- `agent/tools/graph_tools/`: graph, plan, and progress tools.
- `agent/tools/viktor_tools/`: storage and remote app tools.
- `workflow_graph/`: graph state, models, and self-contained WebView renderer.
- `viktor_tools/`: VIKTOR SDK API and storage helpers used by tools.

## Run

```bash
viktor-cli create-app "Workflow Graph Agent" --registered-name workflow-graph-agent
viktor-cli clean-start
```

Set `OPENAI_API_KEY` for chat. Set `TOKEN_VK_APP` or `VIKTOR_TOKEN` before using cross-workspace VIKTOR API calls.

## Calling A DataView

Point `call_remote_viktor_app` at a target entity and DataView method. The tool calls:

```python
entity.compute(method_name="get_data_view", params={...})
```

For a `DataView`, keep `result_key="data"` so the returned `DataResult` payload is stored in `vkt.Storage` for the next tool.

Tools that accept arbitrary JSON use string fields such as `params_json` and `payload_json`. This keeps the OpenAI Agents SDK tool schemas strict while still allowing flexible VIKTOR params and storage payloads.
