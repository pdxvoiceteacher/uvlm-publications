function renderGovernancePanel(data) {
  const panel = document.getElementById('governance-panel');
  if (!panel) return;

  const policies = Array.isArray(data?.policies) ? data.policies : [];

  panel.innerHTML = `
    Active Governance Policies:<br>
    ${policies.map((p) => p.name).join('<br>')}
  `;
}

function loadGovernancePolicies() {
  return fetch('/bridge/governance_policy_map.json', { cache: 'no-store' })
    .then((r) => r.json())
    .then((data) => {
      renderGovernancePanel(data);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-governance');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadGovernancePolicies);
});
