export const deltaResettableClasses = ['delta-forming'];

export function applyDeltaOverlay(cy, enabled = true) {
  cy.elements().removeClass(deltaResettableClasses.join(' '));
  if (!enabled) return;

  cy.elements().addClass('delta-forming');
}

export function bindDeltaOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    applyDeltaOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') reapply();
  });
}
