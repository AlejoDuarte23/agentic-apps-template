import os
from typing import Any

import viktor as vkt


def get_optional_token() -> str | None:
    token = os.getenv("TOKEN_VK_APP") or os.getenv("VIKTOR_TOKEN")
    return token.strip() if token and token.strip() else None


def get_optional_environment() -> str | None:
    environment = os.getenv("VIKTOR_ENVIRONMENT")
    return environment.strip() if environment and environment.strip() else None


def build_api(
    *,
    token: str | None = None,
    environment: str | None = None,
) -> vkt.api_v1.API:
    token = (token or get_optional_token() or "").strip() or None
    environment = (environment or get_optional_environment() or "").strip() or None

    if token and environment:
        return vkt.api_v1.API(token=token, environment=environment)
    if token:
        return vkt.api_v1.API(token=token)
    return vkt.api_v1.API()


class ViktorComputeClient:
    """Small wrapper around vkt.api_v1.Entity.compute for agent tools."""

    def __init__(
        self,
        *,
        token: str | None = None,
        environment: str | None = None,
    ) -> None:
        self.api = build_api(token=token, environment=environment)

    def get_entity(self, *, entity_id: int, workspace_id: int | None = None):
        if workspace_id is None:
            return self.api.get_entity(entity_id)
        return self.api.get_entity(entity_id, workspace_id=workspace_id)

    def compute(
        self,
        *,
        entity_id: int,
        method_name: str,
        params: dict[str, Any] | None,
        workspace_id: int | None = None,
        timeout: int | None = None,
        use_last_saved_params: bool = False,
    ) -> dict[str, Any]:
        entity = self.get_entity(entity_id=entity_id, workspace_id=workspace_id)
        compute_params = entity.last_saved_params if use_last_saved_params else (params or {})
        return entity.compute(
            method_name=method_name,
            params=compute_params,
            timeout=timeout,
        )


def select_compute_result(
    result: dict[str, Any],
    *,
    result_key: str | None = "data",
) -> Any:
    if result_key is None or result_key == "":
        return result
    if result_key not in result:
        keys = ", ".join(sorted(result.keys())) or "<none>"
        raise KeyError(
            f"Compute result does not contain key '{result_key}'. Available keys: {keys}."
        )
    return result[result_key]
