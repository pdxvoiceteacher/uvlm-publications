export const NAVIGATION_CLASSES = {
  highPsi: 'nav-psi-high',
  highRisk: 'nav-risk-high'
};

export const NAVIGATION_RESETTABLE_CLASSES = [
  NAVIGATION_CLASSES.highPsi,
  NAVIGATION_CLASSES.highRisk
];

export function applyNavigationOverlay(cy, state) {
  if (!cy || !state) return;
  if (state.advisory === 'watch' && state.next_state_id) {
    cy.getElementById(state.next_state_id).addClass(NAVIGATION_CLASSES.highPsi);
  }
  if (state.risk === 'high' && state.next_state_id) {
    cy.getElementById(state.next_state_id).addClass(NAVIGATION_CLASSES.highRisk);
  }
}

export function clearNavigationOverlay(cy) {
  if (!cy) return;
  cy.nodes().removeClass(NAVIGATION_CLASSES.highPsi)
    .removeClass(NAVIGATION_CLASSES.highRisk);
}

export function bindNavigationToggle() {
  const toggleEl = document.getElementById('toggle-navigation');
  if (!toggleEl) return;
  toggleEl.addEventListener('change', (e) => {
    if (e.target.checked) {
      const state = window.__bridgeArtifacts?.navigation_state?.result;
      if (state) applyNavigationOverlay(window.cy, state);
    } else {
      clearNavigationOverlay(window.cy);
    }
  });
}
