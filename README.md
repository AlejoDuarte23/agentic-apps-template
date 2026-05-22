# agentic-apps-template

Template repo for building VIKTOR-backed Agents SDK apps with workflow graphs, streamed tool calls, and generated VIKTOR app tools.

## What Is Here

- `viktor-workflow-graph-template/`: the runnable VIKTOR app template with chat, graph WebView, graph tools, and generated VIKTOR tools.
- `convert-app-params-to-schema/`: notebooks that inspect VIKTOR apps and generate JSON artifacts for tool creation.
- `sample_apps/`: two small VIKTOR apps used by the template.
- `SKILL.md`: markdown guidelines for converting generated VIKTOR JSON artifacts into Agents SDK tools.
- `Claude.md`: short instructions for asking Claude to create or update tools from the generated JSON.

Demo apps:

- Reaction loads: https://demo.viktor.ai/workspaces/2672/app/editor/12162
- Footing: https://demo.viktor.ai/workspaces/2673/app/editor/12163

## Environment

Use the same env shape for notebooks and for the template app:

```env
TOKEN_VK_APP=vktrpat_your_viktor_token
VIKTOR_ENVIRONMENT=demo.viktor.ai
```

`TOKEN_VK_APP` is a VIKTOR Personal Access Token. Do not include `Bearer`, quotes, or `Authorization:`.

`VIKTOR_ENVIRONMENT` must be the host only. Use `demo.viktor.ai`, `cloud.viktor.ai`, or `cloud.us1.viktor.ai`. Do not include `https://` or `/api`.

## Generate JSON From A VIKTOR App

1. Create `convert-app-params-to-schema/.env` using the env format above.
2. Run the notebooks:

```bash
jupyter notebook convert-app-params-to-schema/app1_reaction_load_params.ipynb
jupyter notebook convert-app-params-to-schema/app2_reaction_load_params.ipynb
```

Each notebook creates one app folder with:

```text
convert-app-params-to-schema/app1/input_schema.json
convert-app-params-to-schema/app1/available_methods.json
convert-app-params-to-schema/app1/first_method_result.json
convert-app-params-to-schema/app2/input_schema.json
convert-app-params-to-schema/app2/available_methods.json
convert-app-params-to-schema/app2/first_method_result.json
```

The notebooks:

- read saved entity params and declared parametrization defaults;
- merge defaults with saved params;
- list callable methods from views and parametrization actions;
- execute the first data/table method through REST jobs;
- save the input schema, available methods, and first result shape.

## Create A VIKTOR Tool From The JSON

Use either the implemented examples or the markdown guideline:

- Example producer tool: `viktor-workflow-graph-template/agent/tools/viktor_tools/reaction_loads.py`
- Example consumer tool: `viktor-workflow-graph-template/agent/tools/viktor_tools/footing_design.py`
- Guideline: `SKILL.md`

The generated tool should:

- create explicit Pydantic models from `input_schema.json`;
- preserve defaults so `{}` is a valid tool call when the VIKTOR app has defaults;
- use `available_methods.json` to select the VIKTOR method;
- use `first_method_result.json` to understand whether the method returns `data`, `table`, or another payload key;
- call the live app with `vkt.api_v1.API(...).get_workspace(...).get_entity(...).compute(...)`;
- store selected output in `vkt.Storage(..., scope="entity")`;
- expose only user-controlled inputs in downstream tools, reading upstream outputs from storage internally;
- return short JSON tool output with `status`, `message`, `storage_key`, and a compact summary.

## Prompt Claude

Open `Claude.md` and give Claude the app artifact folder you want to implement, for example:

```text
Use Claude.md.
Create an Agents SDK VIKTOR tool from convert-app-params-to-schema/app1.
Use SKILL.md and match the style in viktor-workflow-graph-template/agent/tools/viktor_tools/reaction_loads.py.
Register the tool in viktor-workflow-graph-template/agent/tools/registry.py.
```

For downstream tools, be explicit about storage handoffs:

```text
Create the footing tool from convert-app-params-to-schema/app2.
Expose only pad_thickness.
Read P, My, and Mz from entity-scoped VIKTOR Storage key reaction_loads_table.
Store the footing result at footing_design_data.
```

## Run The Template App

```bash
cd viktor-workflow-graph-template
cp .env.example .env
viktor-cli clean-start
```

The template uses `vkt.ViktorOpenAI`, so no `OPENAI_API_KEY` is needed.
