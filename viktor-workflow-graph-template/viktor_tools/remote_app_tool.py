from typing import Any

from viktor_tools.base import ViktorComputeClient, select_compute_result


def run_remote_viktor_method(
    *,
    workspace_id: int,
    entity_id: int,
    method_name: str,
    params: dict[str, Any],
    result_key: str | None = "data",
    timeout: int | None = None,
    use_last_saved_params: bool = False,
) -> Any:
    client = ViktorComputeClient()
    result = client.compute(
        workspace_id=workspace_id,
        entity_id=entity_id,
        method_name=method_name,
        params=params,
        timeout=timeout,
        use_last_saved_params=use_last_saved_params,
    )
    return select_compute_result(result, result_key=result_key)
