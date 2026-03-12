export const cascadeResettableClasses = ['cascade-strong'];

export function applyCascadeOverlay(cy, signal = 0) {
  cy.elements().removeClass(cascadeResettableClasses.join(' '));

export function applyCascadeOverlay(cy, enabled = true) {
  cy.elements().removeClass(cascadeResettableClasses.join(' '));
  if (!enabled) {
    return;
  }

  cy.nodes().forEach((node) => {
    const health = asNumber(node.data('cascadeHealth'), NaN);
    if (Number.isFinite(health) && health > 0.5) {
      node.addClass('cascade-strong');
    }
  });
}

export function clearCascadeOverlay(cy) {
  cy.elements().removeClass(cascadeResettableClasses.join(' '));
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
