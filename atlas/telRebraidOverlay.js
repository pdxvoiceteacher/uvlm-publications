const REBRAID_THRESHOLD = 0.68;

const REBRAID_RESETTABLE_CLASSES = [
  'rebraid-node',
  'rebraid-coupling-overlay',
  'cascade-strong',
];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applyRebraidOverlay(cy, enabledOrSignal = true) {
  cy.nodes().removeClass(REBRAID_RESETTABLE_CLASSES.join(' '));

  const numericSignal = asNumber(enabledOrSignal, Number.NaN);
  const enabled = Number.isFinite(numericSignal) ? numericSignal > 0 : Boolean(enabledOrSignal);
  if (!enabled) {
    return;
  }

  cy.nodes().forEach((node) => {
    const rebraidPotential = asNumber(node.data('rebraidPotential'), Number.NaN);
    const rebraidAlert = String(node.data('rebraidAlert') ?? '').toLowerCase();

    if (
      rebraidAlert === 'true'
      || rebraidAlert === 'alert'
      || rebraidAlert === 'high'
      || (Number.isFinite(rebraidPotential) && rebraidPotential >= REBRAID_THRESHOLD)
      || (Number.isFinite(numericSignal) && numericSignal > 0.5)
    ) {
      node.addClass('rebraid-node rebraid-coupling-overlay cascade-strong');
      node.data('rebraidAdvisory', 'Advisory only, not authoritative: preliminary mutual translation — non-final advisory.');
    }
  });
}

export function clearRebraidOverlay(cy) {
  cy.nodes().removeClass(REBRAID_RESETTABLE_CLASSES.join(' '));
}

export function bindRebraidOverlayToggle(cy, toggleEl, reapply) {
  const resolvedToggle = toggleEl
    ?? document.getElementById('toggle-rebraid')
    ?? document.getElementById('show-rebraid-signals');
  if (!resolvedToggle) {
    return;
  }

  resolvedToggle.addEventListener('change', () => {
    if (resolvedToggle.checked) {
      applyRebraidOverlay(cy, true);
    } else {
      clearRebraidOverlay(cy);
    }
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}

export function rebraidResettableClasses() {
  return [...REBRAID_RESETTABLE_CLASSES];
}
