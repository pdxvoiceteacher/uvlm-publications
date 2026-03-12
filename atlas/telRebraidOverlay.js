export const rebraidResettableClasses = ['cascade-strong'];

export function applyRebraidOverlay(cy, enabledOrSignal = true) {
  cy.elements().removeClass(rebraidResettableClasses.join(' '));

  const signal = typeof enabledOrSignal === 'number'
    ? enabledOrSignal
    : (enabledOrSignal ? 1 : 0);

  if (signal <= 0) {
    return;
  }

  cy.elements().addClass('cascade-strong');
}

export function clearRebraidOverlay(cy) {
  cy.elements().removeClass(rebraidResettableClasses.join(' '));
}

export function bindRebraidOverlayToggle(cy, toggleEl, reapply) {
  const resolvedToggle = toggleEl
    ?? document.getElementById('toggle-rebraid')
    ?? document.getElementById('show-rebraid-signals');
  if (!resolvedToggle) {
    return;
  }

  resolvedToggle.addEventListener('change', () => {
    applyRebraidOverlay(cy, resolvedToggle.checked ? 1 : 0);
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}
