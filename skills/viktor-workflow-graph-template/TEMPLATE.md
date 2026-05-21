# Code Template

```python
from agent.runner import AgentContext, workflow_agent_sync_stream


class Parametrization(vkt.Parametrization):
    title = vkt.Text("# Workflow Graph Agent")
    chat = vkt.Chat("", method="call_llm")


class Controller(vkt.Controller):
    parametrization = Parametrization

    def call_llm(self, params, entity_id=None, workspace_id=None, **kwargs):
        messages = params.chat.get_messages()
        chat_history = [
            {"role": message["role"], "content": message["content"]}
            for message in messages
        ]
        stream = workflow_agent_sync_stream(
            chat_history,
            context=AgentContext(entity_id=entity_id, workspace_id=workspace_id),
        )
        return vkt.ChatResult(params.chat, stream)

    @vkt.WebView("Workflow Graph", width=100)
    def workflow_view(self, params, **kwargs):
        state = load_canvas_state()
        if state:
            return vkt.WebResult(html=WorkflowViewer(lambda: state).write())
        return vkt.WebResult(html="<!doctype html><html><body></body></html>")
```

```xml
<system>
  <role>You help users run VIKTOR-backed engineering workflows.</role>
  <workflow_rules>
    <rule>Create the graph first with compose_workflow_graph when no graph exists.</rule>
    <rule>Use storage-backed handoffs instead of asking the user to copy JSON.</rule>
  </workflow_rules>
</system>
```

```python
vkt.Storage().set(
    "tool_output_key",
    data=vkt.File.from_data(json.dumps(payload, indent=2)),
    scope="entity",
)

stored_file = vkt.Storage().get("tool_output_key", scope="entity")
payload = json.loads(stored_file.getvalue_binary().decode("utf-8"))
```

```python
api = vkt.api_v1.API(token=os.environ["TOKEN_VK_APP"])
entity = api.get_entity(entity_id, workspace_id=workspace_id)
result = entity.compute(method_name="get_data_view", params=params)
data_view_payload = result["data"]
```

```python
client = ViktorComputeClient()
result = client.compute(
    entity_id=entity_id,
    workspace_id=workspace_id,
    method_name="get_data_view",
    params=params,
)
data_view_payload = select_compute_result(result, result_key="data")
```
