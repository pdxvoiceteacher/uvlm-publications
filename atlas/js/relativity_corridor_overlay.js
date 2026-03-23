async function loadRelativityCorridor() {
  const res = await fetch("/artifacts/relativity_corridor.json", { cache: "no-store" });
  const data = await res.json();

  const panel = document.getElementById("relativity-panel");
  if (!panel) {
    return;
  }

  panel.innerHTML = `
    <h3>Relativity Corridor</h3>
    Score: ${data.score.toFixed(2)}
  `;
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("toggle-relativity-corridor");
  if (!btn) {
    return;
  }

  btn.onclick = loadRelativityCorridor;
});
