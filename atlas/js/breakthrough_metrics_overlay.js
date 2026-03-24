async function loadBreakthroughMetrics() {
  const res = await fetch("/artifacts/breakthrough_metrics.json", { cache: "no-store" });
  const data = await res.json();

  const m = data.metrics;

  const panel = document.getElementById("metrics-panel");
  if (!panel) {
    return;
  }

  panel.innerHTML = `
    <h3>Discovery Prediction Metrics</h3>

    Precision: ${m.precision.toFixed(2)} <br>
    Recall: ${m.recall.toFixed(2)} <br>
    False Positive Rate: ${m.false_positive_rate.toFixed(2)} <br>

    Lead Time Mean: ${m.lead_time_distribution.mean.toFixed(2)} years <br>
    Lead Time Median: ${m.lead_time_distribution.median} years
  `;
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("toggle-breakthrough-metrics");

  if (!btn || btn.dataset.bound === "true") {
    return;
  }

  btn.dataset.bound = "true";
  btn.addEventListener("click", loadBreakthroughMetrics);
});
