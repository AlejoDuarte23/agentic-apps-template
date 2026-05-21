class WorkflowGraph {
  constructor({ stage, edgesSvg, nodesHost, overlayEl }) {
    this.stage = stage;
    this.edgesSvg = edgesSvg;
    this.nodesHost = nodesHost;
    this.overlayEl = overlayEl;
    this.edgesGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    this.edgesSvg.appendChild(this.edgesGroup);

    const rootStyle = getComputedStyle(document.documentElement);
    this.nodeW = parseFloat(rootStyle.getPropertyValue("--node-w")) || 260;
    this.nodeH = parseFloat(rootStyle.getPropertyValue("--node-h")) || 68;
    this.gapX = parseFloat(rootStyle.getPropertyValue("--gap-x")) || 48;
    this.gapY = parseFloat(rootStyle.getPropertyValue("--gap-y")) || 112;

    this.canvasState = { workflow: { nodes: [] }, plan: null, progress: null };
    this.data = { nodes: [] };
    this.byId = new Map();
    this.edges = [];
    this.positions = new Map();
  }

  setData(canvasState) {
    this.canvasState = canvasState || { workflow: { nodes: [] } };
    this.data = this.canvasState.workflow || { nodes: [] };
    this.validateAndBuildGraph();
  }

  validateAndBuildGraph() {
    const nodes = Array.isArray(this.data.nodes) ? this.data.nodes : [];
    this.byId.clear();
    this.edges = [];

    for (const node of nodes) {
      if (!node || typeof node.id !== "string" || !node.id.trim()) {
        throw new Error("Each node needs a non-empty string id.");
      }
      if (this.byId.has(node.id)) {
        throw new Error("Duplicate node id: " + node.id);
      }
      this.byId.set(node.id, node);
    }

    for (const node of nodes) {
      const dependencies = Array.isArray(node.depends_on) ? node.depends_on : [];
      for (const dependency of dependencies) {
        const dependencyId = dependency && dependency.node_id;
        if (!this.byId.has(dependencyId)) {
          throw new Error(`Node "${node.id}" depends on unknown node "${dependencyId}".`);
        }
        this.edges.push({ from: dependencyId, to: node.id });
      }
    }
  }

  topoSort() {
    const nodes = Array.isArray(this.data.nodes) ? this.data.nodes : [];
    const indegree = new Map();
    const outgoing = new Map();
    for (const node of nodes) {
      indegree.set(node.id, 0);
      outgoing.set(node.id, []);
    }
    for (const edge of this.edges) {
      indegree.set(edge.to, (indegree.get(edge.to) || 0) + 1);
      outgoing.get(edge.from).push(edge.to);
    }

    const queue = [];
    for (const [id, degree] of indegree.entries()) {
      if (degree === 0) queue.push(id);
    }

    const order = [];
    while (queue.length) {
      const id = queue.shift();
      order.push(id);
      for (const next of outgoing.get(id)) {
        indegree.set(next, indegree.get(next) - 1);
        if (indegree.get(next) === 0) queue.push(next);
      }
    }
    return order.length === nodes.length ? order : nodes.map((node) => node.id);
  }

  relayout() {
    const order = this.topoSort();
    const depth = new Map();
    for (const id of order) depth.set(id, 0);
    for (const id of order) {
      const node = this.byId.get(id);
      const dependencies = Array.isArray(node.depends_on) ? node.depends_on : [];
      let nextDepth = 0;
      for (const dependency of dependencies) {
        nextDepth = Math.max(nextDepth, (depth.get(dependency.node_id) || 0) + 1);
      }
      depth.set(id, nextDepth);
    }

    const layers = new Map();
    for (const id of order) {
      const layer = depth.get(id) || 0;
      if (!layers.has(layer)) layers.set(layer, []);
      layers.get(layer).push(id);
    }

    this.positions.clear();
    const overlayOffset = this.canvasState.plan || this.canvasState.progress ? 390 : 40;
    const stageW = this.stage.clientWidth || 1000;
    for (const [layer, ids] of layers.entries()) {
      const totalW = ids.length * this.nodeW + Math.max(0, ids.length - 1) * this.gapX;
      const startX = Math.max(overlayOffset, (stageW - totalW) / 2);
      ids.forEach((id, index) => {
        this.positions.set(id, {
          x: startX + index * (this.nodeW + this.gapX),
          y: 52 + layer * (this.nodeH + this.gapY),
        });
      });
    }
  }

  render() {
    this.renderOverlay();
    this.renderNodes();
    this.drawEdges();
  }

  renderOverlay() {
    if (!this.overlayEl) return;
    const plan = this.canvasState.plan;
    const progress = this.canvasState.progress;
    if (!plan && !progress) {
      this.overlayEl.className = "workflow-overlay is-hidden";
      this.overlayEl.innerHTML = "";
      return;
    }
    this.overlayEl.className = "workflow-overlay";
    this.overlayEl.innerHTML = [
      plan ? this.renderPlan(plan) : "",
      progress ? this.renderProgress(progress) : "",
    ].join("");
  }

  renderPlan(plan) {
    const todos = Array.isArray(plan.todos) ? plan.todos : [];
    const done = todos.filter((todo) => todo.status === "completed").length;
    const percent = todos.length ? Math.round((done / todos.length) * 100) : 0;
    return `
      <section class="workflow-card">
        <div class="workflow-card-title">${escapeHtml(plan.title || "Workflow Plan")}</div>
        ${plan.description ? `<div class="workflow-card-description">${escapeHtml(plan.description)}</div>` : ""}
        <div class="workflow-progress-bar"><span style="width:${percent}%"></span></div>
        <div class="workflow-list">
          ${todos.map((todo) => this.renderRow(todo)).join("")}
        </div>
      </section>
    `;
  }

  renderProgress(progress) {
    const steps = Array.isArray(progress.steps) ? progress.steps : [];
    return `
      <section class="workflow-card">
        <div class="workflow-card-title">${escapeHtml(progress.title || "Execution Progress")}</div>
        ${progress.elapsed_time_ms != null ? `<div class="workflow-card-description">${formatMs(progress.elapsed_time_ms)}</div>` : ""}
        <div class="workflow-list">
          ${steps.map((step) => this.renderRow(step)).join("")}
        </div>
      </section>
    `;
  }

  renderRow(item) {
    const status = item.status || "pending";
    return `
      <div class="workflow-row">
        <span class="workflow-dot status-${escapeHtml(status)}"></span>
        <span>
          <div class="workflow-row-label">${escapeHtml(item.label || item.id)}</div>
          ${item.description ? `<div class="workflow-row-description">${escapeHtml(item.description)}</div>` : ""}
        </span>
      </div>
    `;
  }

  renderNodes() {
    const nodes = Array.isArray(this.data.nodes) ? this.data.nodes : [];
    this.nodesHost.innerHTML = "";
    for (const node of nodes) {
      const position = this.positions.get(node.id) || { x: 40, y: 40 };
      const element = document.createElement("div");
      element.className = "workflow-node" + (node.url ? " is-clickable" : "");
      element.style.left = `${position.x}px`;
      element.style.top = `${position.y}px`;
      element.innerHTML = `
        <div class="workflow-node-icon">${escapeHtml(iconText(node.type))}</div>
        <div>
          <div class="workflow-node-title">${escapeHtml(node.title || node.id)}</div>
          <div class="workflow-node-type">${escapeHtml(node.type || "default")}</div>
        </div>
      `;
      if (node.url) {
        element.addEventListener("click", () => window.open(node.url, "_blank", "noopener"));
      }
      this.nodesHost.appendChild(element);
    }
  }

  drawEdges() {
    this.edgesGroup.innerHTML = "";
    for (const edge of this.edges) {
      const from = this.positions.get(edge.from);
      const to = this.positions.get(edge.to);
      if (!from || !to) continue;
      const x1 = from.x + this.nodeW / 2;
      const y1 = from.y + this.nodeH;
      const x2 = to.x + this.nodeW / 2;
      const y2 = to.y;
      const midY = (y1 + y2) / 2;
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`);
      path.setAttribute("fill", "none");
      path.setAttribute("stroke", "var(--edge-color)");
      path.setAttribute("stroke-width", "3");
      path.setAttribute("stroke-linecap", "round");
      this.edgesGroup.appendChild(path);
    }
  }
}

function iconText(type) {
  if (!type || type === "default") return "W";
  return String(type).slice(0, 1).toUpperCase();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatMs(ms) {
  if (ms < 1000) return `${ms} ms`;
  return `${(ms / 1000).toFixed(1)} s`;
}
