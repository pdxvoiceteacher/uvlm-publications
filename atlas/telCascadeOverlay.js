export const cascadeResettableClasses = ['cascade-strong'];

export function applyCascadeOverlay(cy, signal = 0) {
  cy.elements().removeClass(cascadeResettableClasses.join(' '));

  if (signal >= 0.5) {
    cy.elements().addClass('cascade-strong');
  }
}

export function bindCascadeOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) {
    return;
  }
  toggleEl.addEventListener('change', () => {
    applyCascadeOverlay(cy, toggleEl.checked ? 1 : 0);
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}
