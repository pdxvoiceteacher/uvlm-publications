export const riverResettableClasses = ['river-flowing'];

function asNumber(value, fallback = 0) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') {
    const n = Number.parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }
  return fallback;
}

export function applyRiverOverlay(cy) {
  cy.nodes().forEach((node) => {
    const flow = asNumber(node.data('riverFlow'), 0);
    if (flow > 0) {
      node.addClass('river-flowing');
    }
  });
}

export function clearRiverOverlay(cy) {
  cy.nodes().removeClass(riverResettableClasses.join(' '));
}

export function bindRiverOverlayToggle(cy, toggleEl, reapply) {
  const checkbox = toggleEl ?? document.getElementById('toggle-river');
  if (!checkbox) return;

  checkbox.addEventListener('change', () => {
    if (checkbox.checked) applyRiverOverlay(cy);
    else clearRiverOverlay(cy);
    if (typeof reapply === 'function') reapply();
  });
}
