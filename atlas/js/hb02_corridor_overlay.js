async function loadHB02Corridor() {
  const res = await fetch("/artifacts/hb02_corridor_metrics.json", { cache: "no-store" });
  const data = await res.json();

  const panel = document.getElementById("hb02-corridor-panel");
  if (!panel) {
    return;
  }

  panel.innerHTML = `
    <h3>HB-02 DNA Corridor</h3>
    Gradient Strength: ${data.metrics.gradient_strength.toFixed(3)}<br>
    Embedding Convergence: ${data.metrics.embedding_convergence.toFixed(3)}<br>
    Citation Reinforcement: ${data.metrics.citation_reinforcement.toFixed(3)}<br>
    Corridor Score: ${data.metrics.corridor_score.toFixed(3)}
  `;
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("toggle-hb02-corridor");

  if (!btn || btn.dataset.bound === "true") {
    return;
  }

  btn.dataset.bound = "true";
  btn.addEventListener("click", loadHB02Corridor);
});
