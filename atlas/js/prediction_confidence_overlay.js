async function loadPredictionConfidence() {
  const res = await fetch("/artifacts/prediction_confidence.json", { cache: "no-store" });
  const data = await res.json();

  const panel = document.getElementById("confidence-panel");
  if (!panel) {
    return;
  }

  panel.innerHTML = "<h3>Discovery Confidence</h3>";

  data.confidences.forEach((c) => {
    panel.innerHTML += `
      Node: ${c.node}<br>
      Probability: ${c.probability.toFixed(2)}<br><br>
    `;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("toggle-confidence");
  if (!btn) {
    return;
  }

  btn.onclick = loadPredictionConfidence;
});
