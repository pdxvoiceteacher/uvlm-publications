async function loadGlobalCoherenceField() {
  const res = await fetch('/artifacts/global_coherence_field_map.json', {
    cache: 'no-store',
  });
  if (!res.ok) return null;
  return await res.json();
}

function clearGlobalCoherenceFieldOverlay() {
  document.querySelectorAll('.global-coherence-field-panel').forEach((el) => el.remove());
}

function renderGlobalCoherenceFieldPanel(data) {
  const panel = document.createElement('div');
  panel.className = 'global-coherence-field-panel atlas-panel';

  const summary = data.summary || {};
  panel.innerHTML = `
    <h3>Global Coherence Field</h3>
    <p><b>Node Count:</b> ${summary.nodeCount ?? 0}</p>
    <p><b>Max Gradient Magnitude:</b> ${Number(summary.maxGradientMagnitude || 0).toFixed(4)}</p>
  `;
  return panel;
}

async function toggleGlobalCoherenceField() {
  const existing = document.querySelector('.global-coherence-field-panel');
  if (existing) {
    clearGlobalCoherenceFieldOverlay();
    return;
  }

  const data = await loadGlobalCoherenceField();
  if (!data) return;

  const panel = renderGlobalCoherenceFieldPanel(data);
  document.body.appendChild(panel);
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-global-coherence-field');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', toggleGlobalCoherenceField);
});
