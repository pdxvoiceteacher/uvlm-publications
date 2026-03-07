export const zoomLevels = {
  galaxy: 0.8,
  solar: 1.4,
  orbit: 2.1
};

function setVisibility(cy, visibleClasses) {
  const visible = new Set(visibleClasses);
  cy.nodes().forEach((node) => {
    const shouldShow = visible.has(node.data('class'));
    node.toggleClass('zoom-hidden', !shouldShow);
  });

  cy.edges().forEach((edge) => {
    const hide = edge.source().hasClass('zoom-hidden') || edge.target().hasClass('zoom-hidden');
    edge.toggleClass('zoom-hidden', hide);
  });
}

export function applyGalaxyView(cy) {
  setVisibility(cy, ['concept', 'series']);
}

export function applySolarView(cy) {
  setVisibility(cy, ['concept', 'publication', 'series']);
}

export function applyOrbitView(cy) {
  setVisibility(cy, ['concept', 'publication', 'keyword', 'author', 'series']);
}
