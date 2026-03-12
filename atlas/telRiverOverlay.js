export const riverResettableClasses = ['river-flowing'];

export function applyRiverOverlay(cy, enabled = true) {
  cy.elements().removeClass(riverResettableClasses.join(' '));
  if (!enabled) return;

  cy.elements().addClass('river-flowing');
}

export function bindRiverOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    applyRiverOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') reapply();
  });
}
