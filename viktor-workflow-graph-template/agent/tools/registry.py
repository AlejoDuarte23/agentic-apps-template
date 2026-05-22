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
    FootingDesignParams,
    ReactionLoadsParams,
    run_footing_design_func,
    run_reaction_loads_func,
)


TOOL_DISPLAY_NAMES = {
    "compose_workflow_graph": "Compose Workflow Graph",
    "get_workflow_plan": "Get Workflow Plan",
    "set_workflow_plan": "Set Workflow Plan",
    "update_workflow_plan": "Update Workflow Plan",
    "set_workflow_progress": "Set Workflow Progress",
    "run_reaction_loads": "Run Reaction Loads",
    "run_footing_design": "Run Footing Design",
}


def function_tool(name: str, description: str, schema: type[BaseModel], func: Any) -> Any:
    from agents import FunctionTool

    return FunctionTool(
        name=name,
        description=description,
        params_json_schema=schema.model_json_schema(),
        on_invoke_tool=func,
    )


def get_tools() -> list[Any]:
    return [
        function_tool(
            "compose_workflow_graph",
            "Compose a dependency graph and render it in the workflow WebView.",
            ComposeWorkflowGraphArgs,
            compose_workflow_graph_func,
        ),
        function_tool(
            "get_workflow_plan",
            "Read current plan ids and statuses. Call before update_workflow_plan.",
            GetWorkflowPlanArgs,
            get_workflow_plan_func,
        ),
        function_tool(
            "set_workflow_plan",
            "Set or replace the workflow plan shown in the graph overlay.",
            SetWorkflowPlanArgs,
            set_workflow_plan_func,
        ),
        function_tool(
            "update_workflow_plan",
            "Update existing workflow plan items by stable id.",
            UpdateWorkflowPlanArgs,
            update_workflow_plan_func,
        ),
        function_tool(
            "set_workflow_progress",
            "Set, replace, or clear execution progress below the plan.",
            SetWorkflowProgressArgs,
            set_workflow_progress_func,
        ),
        function_tool(
            "run_reaction_loads",
            (
                "Run the demo VIKTOR reaction-load app through the SDK API. "
                "Defaults come from the app parametrization."
            ),
            ReactionLoadsParams,
            run_reaction_loads_func,
        ),
        function_tool(
            "run_footing_design",
            (
                "Run the demo VIKTOR footing app through the SDK API. Reads reactions from "
                "entity-scoped VIKTOR Storage key 'reaction_loads_table'; only pad_thickness "
                "is exposed as a tool input."
            ),
            FootingDesignParams,
            run_footing_design_func,
        ),
    ]
