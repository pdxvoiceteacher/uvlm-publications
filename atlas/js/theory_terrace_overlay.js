async function loadTheoryTerraceMap() {
  const response = await fetch('/bridge/theory_terrace_map.json', { cache: 'no-store' });
  if (!response.ok) return null;
  return await response.json();
}

function clearTheoryTerraceOverlay() {
  if (window.cy) {
    window.cy.nodes('.theory-terrace').removeClass('theory-terrace');
  }

  document.querySelectorAll('.theory-terrace').forEach((node) => {
    node.classList.remove('theory-terrace');
  });
}

function applyTheoryTerraceOverlay(data) {
  const terraces = Array.isArray(data?.terraces) ? data.terraces : [];

  terraces.forEach((t) => {
    const nodeId = String(t?.node ?? '');
    if (!nodeId) return;

    if (window.cy) {
      const cyNode = window.cy.getElementById(nodeId);
      if (cyNode && cyNode.length) {
        cyNode.addClass('theory-terrace');
      }
    }

    const node = document.querySelector(`[data-node="${nodeId}"]`) || document.getElementById(nodeId);
    if (node) {
      node.classList.add('theory-terrace');
    }
  });
}

async function toggleTheoryTerraces() {
  const hasOverlay = Boolean(
    (window.cy && window.cy.nodes('.theory-terrace').length > 0) ||
    document.querySelector('.theory-terrace')
  );

  if (hasOverlay) {
    clearTheoryTerraceOverlay();
    return;
  }

  const data = await loadTheoryTerraceMap();
  if (!data) return;

  applyTheoryTerraceOverlay(data);
}

document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('toggle-theory-terraces');
  if (!button || button.dataset.bound === 'true') return;

  button.dataset.bound = 'true';
  button.addEventListener('click', toggleTheoryTerraces);
});
