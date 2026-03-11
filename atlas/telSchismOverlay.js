const SCHISM_THRESHOLD = 0.7;

const SCHISM_RESETTABLE_CLASSES = [
  'schism-branch',
  'schism-coupling-overlay',
];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applySchismOverlay(cy, enabled = true) {
  cy.nodes().removeClass(SCHISM_RESETTABLE_CLASSES.join(' '));

  if (!enabled) {
    return;
  }

  cy.nodes().forEach((node) => {
    const schismPotential = asNumber(node.data('schismPotential'), NaN);
    const schismAlert = String(node.data('schismAlert') ?? '').toLowerCase();

    if (
      (Number.isFinite(schismPotential) && schismPotential > SCHISM_THRESHOLD)
      || schismAlert === 'true'
      || schismAlert === 'alert'
      || schismAlert === 'high'
    ) {
      node.addClass('schism-branch schism-coupling-overlay');
      node.data('schismAdvisory', 'Advisory only, not authoritative: dual coherence emerging; mutually entangled coherence basins (non-final advisory).');
    }
  });
}

export function bindSchismOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) {
    return;
  }

  toggleEl.addEventListener('change', () => {
    applySchismOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}

export function schismResettableClasses() {
  return [...SCHISM_RESETTABLE_CLASSES];
}
