async function loadHB02DNA() {
  const res = await fetch("/artifacts/dna_corridor_map.json", { cache: "no-store" });
  const data = await res.json();

  const corridors = data.corridors || [];
  const graph = window.cy;

  if (!graph) {
    return;
  }

  corridors.forEach((c) => {
    const node = graph.getElementById(c.node_id);

    if (node && node.length) {
      node.addClass("dna-corridor");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("toggle-hb02-dna");

  if (!btn || btn.dataset.bound === "true") {
    return;
  }

  btn.dataset.bound = "true";
  btn.addEventListener("click", loadHB02DNA);
});
