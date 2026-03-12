export const deltaResettableClasses = ['delta-forming'];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applyDeltaOverlay(cy) {
  cy.nodes().forEach((node) => {
    const strength = asNumber(node.data('deltaStrength'), 0);
    if (strength > 0) {
      node.addClass('delta-forming');
    }
  });
}

export function clearDeltaOverlay(cy) {
  cy.nodes().removeClass(deltaResettableClasses.join(' '));
}

export function bindDeltaOverlayToggle(cy, toggleEl, reapply) {
  const checkbox = toggleEl ?? document.getElementById('toggle-delta');
  if (!checkbox) return;

  checkbox.addEventListener('change', () => {
    if (checkbox.checked) applyDeltaOverlay(cy);
    else clearDeltaOverlay(cy);
    if (typeof reapply === 'function') reapply();
  });
}
