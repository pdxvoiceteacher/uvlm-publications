const RUPTURE_RESETTABLE_CLASSES = ['rupture-node', 'rupture-highlight'];

export function applyRuptureOverlay(cy, enabled = true) {
  cy.nodes().removeClass(RUPTURE_RESETTABLE_CLASSES.join(' '));
  if (!enabled) return;

  cy.nodes().forEach((node) => {
    const ruptureAlert = String(node.data('ruptureAlert') ?? '').toLowerCase();
    if (ruptureAlert === 'true' || ruptureAlert === 'alert' || ruptureAlert === 'high') {
      node.addClass('rupture-node rupture-highlight');
      node.data('ruptureAdvisory', 'Advisory only, not authoritative: rupture signal watch indicator.');
    }
  });
}

export function bindRuptureOverlayToggle(cy, toggleEl, reapply) {
  if (!toggleEl) return;
  toggleEl.addEventListener('change', () => {
    applyRuptureOverlay(cy, Boolean(toggleEl.checked));
    if (typeof reapply === 'function') reapply();
  });
}

export function ruptureResettableClasses() {
  return [...RUPTURE_RESETTABLE_CLASSES];
}
