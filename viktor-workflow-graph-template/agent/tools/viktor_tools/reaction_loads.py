import json
from typing import Any

import viktor as vkt
from pydantic import BaseModel, Field

from agent.tools.viktor_tools.sdk_compute import ViktorSdkComputeClient, select_result_key


REACTION_LOADS_WORKSPACE_ID = 2672
REACTION_LOADS_ENTITY_ID = 12162
REACTION_LOADS_METHOD_NAME = "get_data_view"
REACTION_LOADS_RESULT_KEY = "table"
REACTION_LOADS_STORAGE_KEY = "reaction_loads_table"


class ReactionLoadsInputs(BaseModel):
    distributed_load: float = Field(
        default=25.0,
        description="Distributed load used by the reaction-load app.",
    )
    number_of_reactions: int = Field(
        default=6,
        description="Number of reaction rows to generate.",
    )


class ReactionLoadsParams(BaseModel):
    inputs: ReactionLoadsInputs = Field(
        default_factory=ReactionLoadsInputs,
        description="VIKTOR parametrization payload for the reaction-load app.",
    )


def write_json_to_storage(key: str, payload: Any) -> None:
    vkt.Storage().set(
        key,
        data=vkt.File.from_data(json.dumps(payload, indent=2)),
        scope="entity",
    )


def summarize_table(table: dict[str, Any]) -> dict[str, Any]:
    column_headers = table.get("column_headers") or []
    data = table.get("data") or []
    return {
        "row_count": len(data),
        "columns": [
            header.get("title")
            for header in column_headers
            if isinstance(header, dict) and header.get("title")
        ],
    }


async def run_reaction_loads_func(context: Any, args: str) -> str:
    payload = ReactionLoadsParams.model_validate_json(args or "{}")
    params = payload.model_dump()

    client = ViktorSdkComputeClient()
    result = client.compute_method(
        workspace_id=REACTION_LOADS_WORKSPACE_ID,
        entity_id=REACTION_LOADS_ENTITY_ID,
        method_name=REACTION_LOADS_METHOD_NAME,
        params=params,
    )
    table = select_result_key(result, REACTION_LOADS_RESULT_KEY)
    write_json_to_storage(REACTION_LOADS_STORAGE_KEY, table)

    return json.dumps(
        {
            "status": "completed",
            "method_name": REACTION_LOADS_METHOD_NAME,
            "result_key": REACTION_LOADS_RESULT_KEY,
            "storage_key": REACTION_LOADS_STORAGE_KEY,
            "summary": summarize_table(table),
        },
        indent=2,
    )
