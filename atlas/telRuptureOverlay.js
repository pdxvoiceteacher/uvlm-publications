export const ruptureResettableClasses = ['rupture-looming'];

function asBoolean(value) {
  if (typeof value === 'boolean') return value;
  const normalized = String(value ?? '').toLowerCase();
  return normalized === 'true' || normalized === '1' || normalized === 'yes' || normalized === 'alert' || normalized === 'high';
}

export function applyRuptureOverlay(cy) {
  cy.nodes().forEach((node) => {
    if (asBoolean(node.data('ruptureAlert'))) {
      node.addClass('rupture-looming');
    }
  });
}

export function clearRuptureOverlay(cy) {
  cy.nodes().removeClass(ruptureResettableClasses.join(' '));
}

export function bindRuptureOverlayToggle(cy, toggleEl, reapply) {
  const checkbox = toggleEl ?? document.getElementById('toggle-rupture');
  if (!checkbox) return;

  checkbox.addEventListener('change', () => {
    if (checkbox.checked) applyRuptureOverlay(cy);
    else clearRuptureOverlay(cy);
    if (typeof reapply === 'function') reapply();
  });
}
