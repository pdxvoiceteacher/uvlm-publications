const RIVER_RESETTABLE_CLASSES = ['river-node', 'river-highlight'];

export function applyRiverOverlay(cy, enabled = true) {
  cy.nodes().removeClass(RIVER_RESETTABLE_CLASSES.join(' '));
  if (!enabled) return;

  cy.nodes().forEach((node) => {
    const riverFlow = node.data('riverFlow');
    if (riverFlow) {
      node.addClass('river-node river-highlight');
      node.data('riverAdvisory', 'Advisory only, not authoritative: knowledge-river flow indicator.');
    }
  });
}

export function bindRiverOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    applyRiverOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') reapply();
  });
}

export function riverResettableClasses() {
  return [...RIVER_RESETTABLE_CLASSES];
}
