function renderCivilizationForecastPanel(data) {
  const timeline = Array.isArray(data?.timeline) ? data.timeline : [];
  const panel = document.getElementById('forecast-panel');
  if (!panel) return;

  panel.innerHTML =
    'Century-scale knowledge trajectory:<br>' +
    timeline
      .slice(-10)
      .map((t) => 'Year ' + t.year + ': ' + t.knowledge)
      .join('<br>');
}

function loadCivilizationForecast() {
  return fetch('/artifacts/civilization_forecast.json', { cache: 'no-store' })
    .then((r) => r.json())
    .then((data) => {
      renderCivilizationForecastPanel(data);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-civilization-forecast');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadCivilizationForecast);
});
