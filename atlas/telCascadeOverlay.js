export const cascadeResettableClasses = ['cascade-risk', 'cascade-safe', 'cascade-strong'];

const viabilityThreshold = 1.0;

export function applyCascadeOverlay(cy, signal = 0) {
  cy.elements().removeClass(cascadeResettableClasses.join(' '));

export function applyCascadeOverlay(cy, enabled = true) {
  clearCascadeOverlay(cy);
  if (!enabled) {
    return;
  }

  cy.nodes().forEach((node) => {
    const health = asNumber(node.data('cascadeHealth'), Number.NaN);
    const viability = asNumber(node.data('viabilityScore'), 2.0);

    if (Number.isFinite(viability) && viability <= viabilityThreshold) {
      node.addClass('cascade-risk');
    } else if (Number.isFinite(viability)) {
      node.addClass('cascade-safe');
    }

    if (Number.isFinite(health) && health > 0.5) {
      node.addClass('cascade-strong');
    }
  });
}

export function clearCascadeOverlay(cy) {
  cy.nodes().removeClass(cascadeResettableClasses.join(' '));
}

export function bindCascadeOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) {
    return;
  }
  toggleEl.addEventListener('change', () => {
    if (toggleEl.checked) {
      applyCascadeOverlay(cy, true);
    } else {
      clearCascadeOverlay(cy);
    }
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}
