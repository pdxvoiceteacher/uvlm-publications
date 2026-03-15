function setHealthText(id, label, value, fallback) {
  const element = document.getElementById(id);
  if (!element) {
    return;
  }

  const resolved = value ?? fallback;
  element.textContent = `${label}: ${resolved}`;
}

async function loadTriadicBrainHealth() {
  let payload = null;

  try {
    const response = await fetch('/bridge/triadic_brain_health.json', { cache: 'no-store' });
    if (response.ok) {
      payload = await response.json();
    }
  } catch (_error) {
    payload = null;
  }

  setHealthText('health-kernel', 'Kernel', payload?.kernel, 'stable');
  setHealthText('health-governance', 'Governance', payload?.governance, 'stable');
  setHealthText('health-discovery', 'Discovery', payload?.discovery, 'active');
  setHealthText('health-corridor', 'Corridor Stability', payload?.corridor_stability, 'stable');
  setHealthText('health-swarm', 'Swarm Stability', payload?.swarm_stability, 'stable');

  const alerts = Array.isArray(payload?.governance_alerts)
    ? payload.governance_alerts.join(', ')
    : payload?.governance_alerts;
  setHealthText('health-alerts', 'Alerts', alerts, 'none');
}

document.addEventListener('DOMContentLoaded', () => {
  loadTriadicBrainHealth();
});
