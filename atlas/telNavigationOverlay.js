// Classes for high-psi and high-risk nodes
export const NAVIGATION_CLASSES = ['nav-psi-high', 'nav-risk-high'];
export const NAVIGATION_RESETTABLE_CLASSES = [...NAVIGATION_CLASSES];

export function applyNavigationOverlay(cy, navState) {
  if (!cy) return;
  clearNavigationOverlay(cy);

  const chosen = navState?.chosen_state;
  if (chosen) {
    // Highlight chosen node (high potential)
    const node = cy.nodes(`[id = "${chosen}"]`);
    node.addClass('nav-psi-high');
  }

  // Optionally mark nodes with high decision risk
  cy.nodes().forEach((n) => {
    const data = n.data();
    if (Number(data.nav_risk_score ?? 0) > 1.0) {
      n.addClass('nav-risk-high');
    }
  });
}

export function clearNavigationOverlay(cy) {
  if (!cy) return;
  NAVIGATION_CLASSES.forEach((cls) => {
    cy.elements(`.${cls}`).removeClass(cls);
  });
}

// Toggle binding
export function bindNavigationToggle(toggleElemId) {
  const toggle = document.getElementById(toggleElemId);
  const cy = window.cy;
  if (!toggle || !cy) return;
  toggle.addEventListener('change', () => {
    if (toggle.checked) {
      const navState = window.__bridgeArtifacts?.navigation_state;
      applyNavigationOverlay(cy, navState || {});
    } else {
      clearNavigationOverlay(cy);
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindNavigationToggle = bindNavigationToggle;
}
