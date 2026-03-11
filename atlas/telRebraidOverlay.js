const REBRAID_THRESHOLD = 0.68;

const REBRAID_RESETTABLE_CLASSES = [
  'rebraid-node',
  'rebraid-coupling-overlay',
];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applyRebraidOverlay(cy, enabled = true) {
  cy.nodes().removeClass(REBRAID_RESETTABLE_CLASSES.join(' '));

  if (!enabled) {
    return;
  }

  cy.nodes().forEach((node) => {
    const rebraidPotential = asNumber(node.data('rebraidPotential'), NaN);
    const rebraidAlert = String(node.data('rebraidAlert') ?? '').toLowerCase();

    if (
      rebraidAlert === 'true'
      || rebraidAlert === 'alert'
      || rebraidAlert === 'high'
      || (Number.isFinite(rebraidPotential) && rebraidPotential >= REBRAID_THRESHOLD)
    ) {
      node.addClass('rebraid-node rebraid-coupling-overlay');
      node.data('rebraidAdvisory', 'Advisory only, not authoritative: preliminary mutual translation — non-final advisory.');
    }
  });
}

export function bindRebraidOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) {
    return;
  }

  toggleEl.addEventListener('change', () => {
    applyRebraidOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}

export function rebraidResettableClasses() {
  return [...REBRAID_RESETTABLE_CLASSES];
}
