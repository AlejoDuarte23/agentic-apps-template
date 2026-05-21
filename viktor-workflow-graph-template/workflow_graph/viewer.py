import json
from collections.abc import Callable
from pathlib import Path
from typing import Any


class WorkflowViewer:
    def __init__(self, workflow_factory: Callable[[], Any]) -> None:
        self.workflow_factory = workflow_factory

    def model_dump_value(self, value: Any) -> dict[str, Any]:
        if hasattr(value, "model_dump"):
            return value.model_dump()
        if hasattr(value, "dict"):
            return value.dict()
        raise TypeError("Expected a Pydantic model.")

    def render_html(self) -> str:
        module_dir = Path(__file__).resolve().parent
        css = (module_dir / "styles.css").read_text(encoding="utf-8")
        js = (module_dir / "workflow.js").read_text(encoding="utf-8")
        state = self.workflow_factory()
        state_json = json.dumps(self.model_dump_value(state), ensure_ascii=False).replace(
            "</",
            "<\\/",
        )

        return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Workflow Graph</title>
    <style>{css}</style>
  </head>
  <body>
    <main id="stage">
      <svg id="edges" aria-hidden="true"></svg>
      <div id="nodes"></div>
      <aside id="workflow-overlay" class="workflow-overlay is-hidden"></aside>
    </main>
    <script id="workflow-data" type="application/json">{state_json}</script>
    <script>{js}</script>
    <script>
      const dataEl = document.getElementById("workflow-data");
      const state = JSON.parse(dataEl.textContent || "{{}}");
      const graph = new WorkflowGraph({{
        stage: document.getElementById("stage"),
        edgesSvg: document.getElementById("edges"),
        nodesHost: document.getElementById("nodes"),
        overlayEl: document.getElementById("workflow-overlay"),
      }});
      graph.setData(state);
      graph.relayout();
      graph.render();
      window.addEventListener("resize", () => {{
        graph.relayout();
        graph.render();
      }});
    </script>
  </body>
</html>
"""

    def write(self) -> str:
        return self.render_html()
