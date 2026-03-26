async function loadHB02Breakthrough() {
  const res = await fetch("/artifacts/hb02_breakthrough_result.json", { cache: "no-store" });
  const data = await res.json();

  const panel = document.getElementById("hb02-breakthrough-panel");
  if (!panel) {
    return;
  }

  panel.innerHTML = `
    <h3>HB-02 Breakthrough Test</h3>
    Corridor Year: ${data.result.corridor_year}<br>
    Breakthrough Year: ${data.result.breakthrough_year}<br>
    Lead Time: ${data.result.lead_time_years} years<br>
    Prediction: ${data.result.predicted ? "YES" : "NO"}
  `;
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("toggle-hb02-breakthrough");

  if (!btn || btn.dataset.bound === "true") {
    return;
  }

  btn.dataset.bound = "true";
  btn.addEventListener("click", loadHB02Breakthrough);
});
