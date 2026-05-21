import json
from typing import Any

from pydantic import BaseModel, Field

from viktor_tools.storage import read_json_from_storage, write_json_to_storage


class StorageWriteArgs(BaseModel):
    key: str = Field(..., description="Entity storage key.")
    payload_json: str = Field(
        ...,
        description="JSON string to write to entity storage.",
    )


class StorageReadArgs(BaseModel):
    key: str = Field(..., description="Entity storage key.")


async def write_storage_json_func(context: Any, args: str) -> str:
    payload = StorageWriteArgs.model_validate_json(args)
    try:
        value: Any = json.loads(payload.payload_json)
    except json.JSONDecodeError as exc:
        raise ValueError(f"payload_json must be valid JSON: {exc}") from exc
    write_json_to_storage(payload.key, value)
    return f"Stored JSON in entity storage key '{payload.key}'."


async def read_storage_json_func(context: Any, args: str) -> str:
    payload = StorageReadArgs.model_validate_json(args)
    return json.dumps(read_json_from_storage(payload.key), indent=2)
