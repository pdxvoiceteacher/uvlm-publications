export const rebraidResettableClasses = ['rebraid-strong'];

function asBoolean(value) {
  if (typeof value === 'boolean') return value;
  const normalized = String(value ?? '').toLowerCase();
  return normalized === 'true' || normalized === '1' || normalized === 'yes' || normalized === 'alert' || normalized === 'high';
}

export function applyRebraidOverlay(cy, enabled = true) {
  cy.elements().removeClass(rebraidResettableClasses.join(' '));
  if (!enabled) {
    return;
  }

  cy.nodes().forEach((node) => {
    if (asBoolean(node.data('rebraidAlert'))) {
      node.addClass('rebraid-strong');
    }
  });
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
    applyRebraidOverlay(cy, Boolean(resolvedToggle.checked));
    if (typeof reapply === 'function') {
      reapply();
    }
  });
}
