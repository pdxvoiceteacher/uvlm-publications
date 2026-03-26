async function loadHB01Relativity() {
  const res = await fetch("/artifacts/relativity_corridor_map.json", { cache: "no-store" });
  const data = await res.json();

  const vectors = data.vectors || [];
  const graph = window.cy;

  if (!graph) {
    return;
  }

  vectors.forEach((v) => {
    const node = graph.getElementById(v.node_id);

    if (node && node.length) {
      node.addClass("relativity-corridor");

      const edgeId = `vec_${v.node_id}`;
      if (!graph.getElementById(edgeId).length) {
        graph.add({
          group: "edges",
          data: {
            id: edgeId,
            source: v.node_id,
            target: v.node_id,
            dx: v.dx,
            dy: v.dy
          }
        });
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("toggle-hb01-relativity");

  if (!btn || btn.dataset.bound === "true") {
    return;
  }

  btn.dataset.bound = "true";
  btn.addEventListener("click", loadHB01Relativity);
});
