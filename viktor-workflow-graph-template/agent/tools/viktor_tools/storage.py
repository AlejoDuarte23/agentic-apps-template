import json
from typing import Any

from pydantic import Field

from agent.tools.base import Tool
from viktor_tools.storage import read_json_from_storage, write_json_to_storage


class StorageWriteArgs(Tool):
    key: str = Field(..., description="Entity storage key.")
    payload: dict[str, Any] = Field(..., description="JSON-serializable payload.")


class StorageReadArgs(Tool):
    key: str = Field(..., description="Entity storage key.")


async def write_storage_json_func(_ctx: Any, args: str) -> str:
    payload = StorageWriteArgs.model_validate_json(args)
    write_json_to_storage(payload.key, payload.payload)
    return f"Stored JSON in entity storage key '{payload.key}'."


async def read_storage_json_func(_ctx: Any, args: str) -> str:
    payload = StorageReadArgs.model_validate_json(args)
    return json.dumps(read_json_from_storage(payload.key), indent=2)
