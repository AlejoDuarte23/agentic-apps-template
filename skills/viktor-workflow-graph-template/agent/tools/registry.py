from typing import Any

from pydantic import BaseModel

from agent.tools.graph_tools import (
    ComposeWorkflowGraphArgs,
    GetWorkflowPlanArgs,
    SetWorkflowPlanArgs,
    SetWorkflowProgressArgs,
    UpdateWorkflowPlanArgs,
    compose_workflow_graph_func,
    get_workflow_plan_func,
    set_workflow_plan_func,
    set_workflow_progress_func,
    update_workflow_plan_func,
)
from agent.tools.viktor_tools import (
    CallRemoteViktorAppArgs,
    StorageReadArgs,
    StorageWriteArgs,
    call_remote_viktor_app_func,
    read_storage_json_func,
    write_storage_json_func,
)


TOOL_DISPLAY_NAMES = {
    "compose_workflow_graph": "Compose Workflow Graph",
    "get_workflow_plan": "Get Workflow Plan",
    "set_workflow_plan": "Set Workflow Plan",
    "update_workflow_plan": "Update Workflow Plan",
    "set_workflow_progress": "Set Workflow Progress",
    "write_storage_json": "Write Storage JSON",
    "read_storage_json": "Read Storage JSON",
    "call_remote_viktor_app": "Call Remote VIKTOR App",
}


def _function_tool(name: str, description: str, schema: type[BaseModel], func: Any) -> Any:
    from agents import FunctionTool

    return FunctionTool(
        name=name,
        description=description,
        params_json_schema=schema.model_json_schema(),
        on_invoke_tool=func,
    )


def get_tools() -> list[Any]:
    return [
        _function_tool(
            "compose_workflow_graph",
            "Compose a dependency graph and render it in the workflow WebView.",
            ComposeWorkflowGraphArgs,
            compose_workflow_graph_func,
        ),
        _function_tool(
            "get_workflow_plan",
            "Read current plan ids and statuses. Call before update_workflow_plan.",
            GetWorkflowPlanArgs,
            get_workflow_plan_func,
        ),
        _function_tool(
            "set_workflow_plan",
            "Set or replace the workflow plan shown in the graph overlay.",
            SetWorkflowPlanArgs,
            set_workflow_plan_func,
        ),
        _function_tool(
            "update_workflow_plan",
            "Update existing workflow plan items by stable id.",
            UpdateWorkflowPlanArgs,
            update_workflow_plan_func,
        ),
        _function_tool(
            "set_workflow_progress",
            "Set, replace, or clear execution progress below the plan.",
            SetWorkflowProgressArgs,
            set_workflow_progress_func,
        ),
        _function_tool(
            "write_storage_json",
            "Write a JSON payload into entity-scoped vkt.Storage.",
            StorageWriteArgs,
            write_storage_json_func,
        ),
        _function_tool(
            "read_storage_json",
            "Read JSON from entity-scoped vkt.Storage.",
            StorageReadArgs,
            read_storage_json_func,
        ),
        _function_tool(
            "call_remote_viktor_app",
            (
                "Call a VIKTOR entity method with vkt.api_v1.Entity.compute and store the selected "
                "result payload. For DataView methods, keep result_key='data'."
            ),
            CallRemoteViktorAppArgs,
            call_remote_viktor_app_func,
        ),
    ]
