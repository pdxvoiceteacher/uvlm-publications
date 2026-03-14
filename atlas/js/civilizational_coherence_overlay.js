async function loadCivilizationalCoherence() {
  const res = await fetch('/artifacts/civilizational_coherence_map.json', {
    cache: 'no-store',
  });
  if (!res.ok) return null;
  return await res.json();
}

function clearCivilizationalCoherenceOverlay() {
  document.querySelectorAll('.civilizational-coherence-panel').forEach((el) => el.remove());
}

function renderCivilizationalCoherencePanel(data) {
  const panel = document.createElement('div');
  panel.className = 'civilizational-coherence-panel atlas-panel';

  const metrics = data.metrics || {};
  const regime = (data.summary || {}).regime || 'unknown';

  panel.innerHTML = `
    <h3>Civilizational Coherence</h3>
    <p><b>Regime:</b> ${regime}</p>
    <p><b>S_civ:</b> ${Number(metrics.S_civ || 0).toFixed(4)}</p>
    <p><b>Psi:</b> ${Number(metrics.Psi || 0).toFixed(4)}</p>
    <p><b>Plurality:</b> ${Number(metrics.Plurality || 0).toFixed(4)}</p>
    <p><b>Trust:</b> ${Number(metrics.Trust || 0).toFixed(4)}</p>
    <p><b>Memory:</b> ${Number(metrics.Memory || 0).toFixed(4)}</p>
    <p><b>Discovery Gradient:</b> ${Number(metrics.DiscoveryGradient || 0).toFixed(4)}</p>
    <p><b>Entropy:</b> ${Number(metrics.Entropy || 0).toFixed(4)}</p>
    <p><b>Capture:</b> ${Number(metrics.Capture || 0).toFixed(4)}</p>
  `;

  if (regime === 'healthy_discovery') panel.classList.add('status-good');
  if (regime === 'critical_boundary') panel.classList.add('status-watch');
  if (regime === 'orthodoxy_collapse' || regime === 'fragmentation_noise' || regime === 'civilizational_rupture') {
    panel.classList.add('status-warn');
  }

  return panel;
}

async function toggleCivilizationalCoherence() {
  const existing = document.querySelector('.civilizational-coherence-panel');
  if (existing) {
    clearCivilizationalCoherenceOverlay();
    return;
  }

  const data = await loadCivilizationalCoherence();
  if (!data) return;

  const panel = renderCivilizationalCoherencePanel(data);
  document.body.appendChild(panel);
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-civilizational-coherence');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', toggleCivilizationalCoherence);
});
