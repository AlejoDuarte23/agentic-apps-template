import json
from typing import Any

import viktor as vkt


def write_json_to_storage(key: str, payload: Any) -> None:
    vkt.Storage().set(
        key,
        data=vkt.File.from_data(json.dumps(payload, indent=2)),
        scope="entity",
    )


def read_json_from_storage(key: str) -> Any:
    stored_file = vkt.Storage().get(key, scope="entity")
    raw = stored_file.getvalue_binary().decode("utf-8")
    return json.loads(raw)


def delete_storage_key(key: str) -> None:
    try:
        vkt.Storage().delete(key, scope="entity")
    except Exception:
        pass
