function renderCulturalTransmissionPanel(data) {
  const panel = document.getElementById('cultural-panel');
  if (!panel) return;

  const metrics = data?.metrics || {};

  panel.innerHTML = `
  Cultural Influence Metrics<br>
  Education: ${metrics.education}<br>
  Media: ${metrics.media}<br>
  Understanding: ${metrics.understanding}
  `;
}

function loadCulturalTransmission() {
  return fetch('/artifacts/cultural_transmission_map.json', { cache: 'no-store' })
    .then((r) => r.json())
    .then((data) => {
      renderCulturalTransmissionPanel(data);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-cultural-transmission');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadCulturalTransmission);
});
