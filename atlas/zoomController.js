import { zoomLevels, applyGalaxyView, applySolarView, applyOrbitView } from './zoomLevels.js';
import { applySolarSystemLayout, applyOrbitDetailLayout } from './layoutEngine.js';

function activeConcept(cy) {
  const selected = cy.nodes('.highlight').filter((n) => n.data('class') === 'concept');
  return selected.length ? selected[0].id() : null;
}

function activePublication(cy) {
  const selected = cy.nodes('.highlight').filter((n) => n.data('class') === 'publication');
  return selected.length ? selected[0].id() : null;
}

function animatePositions(cy, positions, duration = 500) {
  Object.entries(positions).forEach(([id, pos]) => {
    const node = cy.getElementById(id);
    if (node && node.length) {
      node.animate({ position: pos }, { duration });
    }
  });
}

function applyForZoom(cy) {
  const z = cy.zoom();

  if (z < zoomLevels.galaxy) {
    applyGalaxyView(cy);
    return;
  }

  if (z < zoomLevels.solar) {
    applySolarView(cy);
    const conceptId = activeConcept(cy);
    if (conceptId) {
      animatePositions(cy, applySolarSystemLayout(cy, conceptId));
    }
    return;
  }

  applyOrbitView(cy);
  const publicationId = activePublication(cy);
  if (publicationId) {
    animatePositions(cy, applyOrbitDetailLayout(cy, publicationId));
  }
}

export function bindZoomController(cy) {
  cy.on('zoom', () => applyForZoom(cy));
  applyForZoom(cy);

  return {
    toGalaxy: () => {
      applyGalaxyView(cy);
      cy.animate({ zoom: Math.max(zoomLevels.galaxy * 0.9, 0.5) }, { duration: 450 });
      cy.fit(cy.elements(':visible'), 80);
    },
    toSolar: (conceptId) => {
      applySolarView(cy);
      if (conceptId) {
        animatePositions(cy, applySolarSystemLayout(cy, conceptId));
        const concept = cy.getElementById(conceptId);
        cy.animate({ zoom: zoomLevels.solar + 0.05, center: { eles: concept } }, { duration: 500 });
      }
    },
    toOrbit: (publicationId) => {
      applyOrbitView(cy);
      if (publicationId) {
        animatePositions(cy, applyOrbitDetailLayout(cy, publicationId));
        const pub = cy.getElementById(publicationId);
        cy.animate({ zoom: zoomLevels.orbit + 0.2, center: { eles: pub } }, { duration: 500 });
      }
    }
  };
}
