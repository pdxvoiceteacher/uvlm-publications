async function loadGovernanceStability() {
  const res = await fetch('/artifacts/governance_stability_map.json', {
    cache: 'no-store'
  });

  const data = await res.json();

  renderGovernancePanel(data);
}

function renderGovernancePanel(data) {
  let panel = document.getElementById('governance-stability-panel');

  if (!panel) {
    panel = document.createElement('div');
    panel.id = 'governance-stability-panel';
    panel.className = 'atlas-panel';
    document.body.appendChild(panel);
  }

  const regime = data?.regime ?? 'unknown';
  const stabilityScore = Number(data?.stability_score ?? 0);

  panel.innerHTML = `
        <h3>Governance Stability</h3>
        <p>Regime: ${regime}</p>
        <p>Stability Score: ${stabilityScore.toFixed(3)}</p>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-governance-stability');

  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadGovernanceStability);
});
