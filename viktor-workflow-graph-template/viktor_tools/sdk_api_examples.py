import os
from typing import Any

import viktor as vkt


def read_current_entity_parent_params(entity_id: int) -> dict[str, Any]:
    api = vkt.api_v1.API()
    current_entity = api.get_entity(entity_id)
    return dict(current_entity.parent().last_saved_params)


def compute_entity_method_in_current_workspace(
    *,
    entity_id: int,
    method_name: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    api = vkt.api_v1.API()
    entity = api.get_entity(entity_id)
    return entity.compute(method_name=method_name, params=params)


def compute_entity_method_cross_workspace(
    *,
    workspace_id: int,
    entity_id: int,
    method_name: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    token = os.environ["TOKEN_VK_APP"]
    api = vkt.api_v1.API(token=token)
    entity = api.get_workspace(workspace_id).get_entity(entity_id)
    return entity.compute(method_name=method_name, params=params)


def compute_remote_data_view(
    *,
    workspace_id: int,
    entity_id: int,
    method_name: str,
    params: dict[str, Any],
) -> Any:
    result = compute_entity_method_cross_workspace(
        workspace_id=workspace_id,
        entity_id=entity_id,
        method_name=method_name,
        params=params,
    )
    return result["data"]
