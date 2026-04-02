async function loadCorridorSeries() {
  const res = await fetch("/artifacts/relativity_corridor_map.json");
  return await res.json();
}

function renderCorridorSeries(data) {
  const panel = document.getElementById("corridor-series-panel");
  if (!panel) {
    return;
  }

  panel.innerHTML = "<h3>Discovery Convergence</h3>";

  (data.series || []).forEach(([year, value]) => {
    const el = document.createElement("div");
    el.textContent = `${year}: ${value.toFixed(3)}`;
    panel.appendChild(el);
  });
}

document.getElementById("toggle-corridor-series")
  ?.addEventListener("click", async () => {
    const data = await loadCorridorSeries();
    renderCorridorSeries(data);
  });
