async function loadSwarmDiscoveries() {
  const res = await fetch('/bridge/swarm_discoveries.json', { cache: 'no-store' });
  if (!res.ok) return null;
  return await res.json();
}

function extractConvergedNodeIds(payload) {
  const candidates = payload?.nodes || payload?.discoveries || payload?.entries || [];
  return candidates
    .filter((entry) => {
      if (typeof entry === 'string') return true;
      const convergence = Number(entry?.convergence_count ?? entry?.agent_count ?? entry?.agents ?? 0);
      return convergence >= 2;
    })
    .map((entry) => (typeof entry === 'string' ? entry : String(entry.id ?? entry.node_id ?? '')))
    .filter(Boolean);
}

function clearSwarmDiscoveryOverlay() {
  if (window.cy) {
    window.cy.nodes('.swarm-discovery').removeClass('swarm-discovery');
  }

  document.querySelectorAll('.swarm-discovery').forEach((el) => {
    el.classList.remove('swarm-discovery');
  });
}

function applySwarmDiscoveryOverlay(nodeIds) {
  if (window.cy) {
    nodeIds.forEach((nodeId) => {
      const node = window.cy.getElementById(nodeId);
      if (node && node.length) node.addClass('swarm-discovery');
    });
  }

  nodeIds.forEach((nodeId) => {
    const node = document.getElementById(nodeId);
    if (node) {
      node.classList.add('swarm-discovery');
    }
  });
}

async function toggleSwarmDiscoveries() {
  const hasOverlay = Boolean(
    (window.cy && window.cy.nodes('.swarm-discovery').length > 0) || document.querySelector('.swarm-discovery')
  );

  if (hasOverlay) {
    clearSwarmDiscoveryOverlay();
    return;
  }

  const payload = await loadSwarmDiscoveries();
  if (!payload) return;

  const nodeIds = extractConvergedNodeIds(payload);
  applySwarmDiscoveryOverlay(nodeIds);
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-swarm-discoveries');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', toggleSwarmDiscoveries);
});
