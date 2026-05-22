# Claude.md

Use this repo to create VIKTOR-backed Agents SDK tools from notebook-generated JSON.

## Context

The VIKTOR app template is in `viktor-workflow-graph-template/`.

The generated app artifacts are in `convert-app-params-to-schema/<app>/`:

- `input_schema.json`
- `available_methods.json`
- `first_method_result.json`

The conversion guideline is `SKILL.md`.

Implemented references:

- Producer tool: `viktor-workflow-graph-template/agent/tools/viktor_tools/reaction_loads.py`
- Consumer/storage handoff tool: `viktor-workflow-graph-template/agent/tools/viktor_tools/footing_design.py`
- SDK helper: `viktor-workflow-graph-template/agent/tools/viktor_tools/sdk_compute.py`
- Tool registry: `viktor-workflow-graph-template/agent/tools/registry.py`

## Environment

Use this exact env shape for notebooks and local app runs:

```env
TOKEN_VK_APP=vktrpat_your_viktor_token
VIKTOR_ENVIRONMENT=demo.viktor.ai
```

`VIKTOR_ENVIRONMENT` is host-only. Do not use `https://demo.viktor.ai` or `https://demo.viktor.ai/api`.

The app uses `vkt.ViktorOpenAI` for the LLM. Do not add `OPENAI_API_KEY`.

## Tool Creation Workflow

1. Read the selected app folder.
2. Read `available_methods.json` and identify the callable method.
3. If there is more than one method, ask which method to implement.
4. Read `input_schema.json` and create explicit Pydantic models.
5. Preserve defaults from the schema. The tool should work with `{}` when the app has defaults.
6. Read `first_method_result.json` to choose the result key.
7. Prefer result keys in this order: `data`, `table`, `download`, `geometry`, `plotly`, `geojson`, `web`, `pdf`, `image`, `ifc`, `optimization`, `set_params`.
8. Call the live VIKTOR app through SDK compute, not a static JSON fixture.
9. Store the selected result with `vkt.Storage().set(..., scope="entity")`.
10. Register the tool in `agent/tools/registry.py`.
11. Return short JSON output with `status`, `message`, `storage_key`, and a compact summary.

## Storage Handoff Rules

For producer tools:

- expose the VIKTOR app input params;
- call the VIKTOR method;
- store the selected output under a stable key.

For downstream tools:

- expose only user-controlled inputs;
- read upstream output internally from entity-scoped `vkt.Storage`;
- return `status="needs_prerequisite"` with `retry_action.tool` if the storage key is missing.

Current handoff:

```text
run_reaction_loads -> reaction_loads_table
run_footing_design reads reaction_loads_table -> footing_design_data
```

## Claude Prompt Template

```text
Create an Agents SDK VIKTOR tool from <artifact-folder>.

Use:
- SKILL.md
- <artifact-folder>/input_schema.json
- <artifact-folder>/available_methods.json
- <artifact-folder>/first_method_result.json
- viktor-workflow-graph-template/agent/tools/viktor_tools/reaction_loads.py as the producer-tool style
- viktor-workflow-graph-template/agent/tools/viktor_tools/footing_design.py if this tool consumes a previous storage output

Requirements:
- Ask which method to implement if available_methods.json has multiple methods.
- Build explicit Pydantic models with defaults.
- Use ViktorSdkComputeClient for live compute.
- Store selected output in entity-scoped vkt.Storage.
- Return recoverable failures as JSON tool output.
- Register the tool in agent/tools/registry.py.
- Keep the implementation small and match the existing style.
```

## Validation

Run:

```bash
python3 -m py_compile $(rg --files viktor-workflow-graph-template -g '*.py') $(rg --files sample_apps -g '*.py')
node --check --input-type=module < viktor-workflow-graph-template/workflow_graph/workflow.js
xmllint --noout viktor-workflow-graph-template/agent/system_prompt.xml
git diff --check
```
