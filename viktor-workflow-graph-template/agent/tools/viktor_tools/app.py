import os
from typing import Any

from pydantic import Field

from agent.tools.base import Tool
from viktor_tools.remote_app_tool import run_remote_viktor_method
from viktor_tools.storage import read_json_from_storage, write_json_to_storage


class CallRemoteViktorAppArgs(Tool):
    workspace_id: int = Field(
        default_factory=lambda: int(os.getenv("VIKTOR_REMOTE_WORKSPACE_ID", "0") or 0),
        description="Target VIKTOR workspace id.",
    )
    entity_id: int = Field(
        default_factory=lambda: int(os.getenv("VIKTOR_REMOTE_ENTITY_ID", "0") or 0),
        description="Target VIKTOR entity id.",
    )
    method_name: str = Field(
        default_factory=lambda: os.getenv("VIKTOR_REMOTE_METHOD_NAME", "get_data_view"),
        description="Target DataView or button method name.",
    )
    params: dict[str, Any] = Field(default_factory=dict)
    use_last_saved_params: bool = Field(
        default=False,
        description="Use the target entity's last_saved_params instead of params.",
    )
    input_storage_key: str | None = Field(
        default=None,
        description="Optional storage key to merge into params before the call.",
    )
    result_key: str | None = Field(
        default="data",
        description=(
            "Compute result key to store. Use 'data' for DataView/DataResult output, "
            "or null/empty string to store the full compute result."
        ),
    )
    timeout: int | None = Field(
        default=None,
        ge=1,
        description="Optional VIKTOR compute timeout in seconds.",
    )
    output_storage_key: str = Field(
        default="remote_viktor_dataview_result",
        description="Storage key for the selected compute result payload.",
    )


async def call_remote_viktor_app_func(_ctx: Any, args: str) -> str:
    payload = CallRemoteViktorAppArgs.model_validate_json(args)
    if not payload.workspace_id or not payload.entity_id:
        raise ValueError("workspace_id and entity_id are required.")

    params = dict(payload.params)
    if payload.input_storage_key:
        params.update(read_json_from_storage(payload.input_storage_key))

    result = run_remote_viktor_method(
        workspace_id=payload.workspace_id,
        entity_id=payload.entity_id,
        method_name=payload.method_name,
        params=params,
        result_key=payload.result_key,
        timeout=payload.timeout,
        use_last_saved_params=payload.use_last_saved_params,
    )
    write_json_to_storage(payload.output_storage_key, result)
    return (
        f"Remote VIKTOR compute '{payload.method_name}' completed. "
        f"Result stored at '{payload.output_storage_key}'."
    )
