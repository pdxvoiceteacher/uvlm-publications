const CASCADE_THRESHOLD = 1.0;
const CASCADE_RESETTABLE_CLASSES = ['cascade-strong'];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applyCascadeOverlay(cy, enabled = true) {
  cy.elements().removeClass(CASCADE_RESETTABLE_CLASSES.join(' '));
  if (!enabled) {
    return;
  }

  cy.elements().forEach((ele) => {
    const signal = asNumber(ele.data('cascadeSignal'), NaN);
    if (Number.isFinite(signal) && signal >= CASCADE_THRESHOLD) {
      ele.addClass('cascade-strong');
      ele.data('cascadeAdvisory', 'Advisory only, not authoritative: cascade hotspot (strong propagation) indicator.');
    }
  });
}

export function bindCascadeOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) {
    return;
  }
  toggleEl.addEventListener('change', () => {
    applyCascadeOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}

export function cascadeResettableClasses() {
  return [...CASCADE_RESETTABLE_CLASSES];
}
