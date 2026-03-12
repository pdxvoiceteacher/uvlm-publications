const CORRIDOR_THRESHOLD = 0.65;
const CORRIDOR_RESETTABLE_CLASSES = ['corridor-node', 'corridor-highlight'];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applyCorridorOverlay(cy, enabled = true) {
  cy.nodes().removeClass(CORRIDOR_RESETTABLE_CLASSES.join(' '));
  if (!enabled) return;

  cy.nodes().forEach((node) => {
    const potential = asNumber(node.data('corridorPotential'), NaN);
    const isExploring = Boolean(node.data('isExploring'));
    if (isExploring || (Number.isFinite(potential) && potential >= CORRIDOR_THRESHOLD)) {
      node.addClass('corridor-node corridor-highlight');
      node.data('corridorAdvisory', 'Advisory only, not authoritative: preliminary plural exploration zone.');
    }
  });
}

export function bindCorridorOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    applyCorridorOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') reapply();
  });
}

export function corridorResettableClasses() {
  return [...CORRIDOR_RESETTABLE_CLASSES];
}
