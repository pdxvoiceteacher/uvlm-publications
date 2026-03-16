async function loadPhaseDiagram() {
  const res = await fetch('/artifacts/governance_phase_diagram.json', { cache: 'no-store' });
  const data = await res.json();
  renderPhaseDiagram(data.surface || []);
}

function renderPhaseDiagram(surface) {
  let panel = document.getElementById('phase-diagram-panel');

  if (!panel) {
    panel = document.createElement('div');
    panel.id = 'phase-diagram-panel';
    panel.className = 'atlas-panel';
    document.body.appendChild(panel);
  }

  const counts = {};

  surface.forEach((p) => {
    counts[p.regime] = (counts[p.regime] || 0) + 1;
  });

  panel.innerHTML = `
        <h3>Civilizational Stability Phase Diagram</h3>
        <p>Golden Age: ${counts.golden_age || 0}</p>
        <p>Stable Discovery: ${counts.stable_discovery || 0}</p>
        <p>Orthodoxy Drift: ${counts.orthodoxy_drift || 0}</p>
        <p>Fragmentation: ${counts.fragmentation || 0}</p>
        <p>Civilizational Rupture: ${counts.civilizational_rupture || 0}</p>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-phase-diagram');
  if (!btn || btn.dataset.bound === 'true') return;
  btn.dataset.bound = 'true';
  document.getElementById('toggle-phase-diagram').addEventListener('click', loadPhaseDiagram);
});
