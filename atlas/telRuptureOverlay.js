export const ruptureResettableClasses = ['rupture-looming'];

export function applyRuptureOverlay(cy, enabled = true) {
  cy.elements().removeClass(ruptureResettableClasses.join(' '));
  if (!enabled) return;

  cy.elements().addClass('rupture-looming');
}

export function bindRuptureOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    applyRuptureOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') reapply();
  });
}
