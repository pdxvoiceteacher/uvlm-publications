const DELTA_THRESHOLD = 0.66;
const DELTA_RESETTABLE_CLASSES = ['delta-node', 'delta-highlight'];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applyDeltaOverlay(cy, enabled = true) {
  cy.nodes().removeClass(DELTA_RESETTABLE_CLASSES.join(' '));
  if (!enabled) return;

  cy.nodes().forEach((node) => {
    const isDeltaNode = Boolean(node.data('isDeltaNode'));
    const deltaPotential = asNumber(node.data('deltaPotential'), NaN);
    if (isDeltaNode || (Number.isFinite(deltaPotential) && deltaPotential >= DELTA_THRESHOLD)) {
      node.addClass('delta-node delta-highlight');
      node.data('deltaAdvisory', 'Advisory only, not authoritative: civilizational delta emergence signal.');
    }
  });
}

export function bindDeltaOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    applyDeltaOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') reapply();
  });
}

export function deltaResettableClasses() {
  return [...DELTA_RESETTABLE_CLASSES];
}
