export const NAVIGATION_CLASSES = ['nav-psi-high', 'nav-risk-high'];

export const NAVIGATION_RESETTABLE_CLASSES = [...NAVIGATION_CLASSES];

export function applyNavigationOverlay(cy, state) {
  if (!cy || !state) return;
  const chosen = state.chosen_state ?? state.result?.chosen_state ?? {};
  const psi = chosen.psi ?? 0;
  if (psi > 0.8) {
    cy.nodes().addClass('nav-psi-high');
  }
  if ((chosen.lambda_critical ?? 0) > 0.8) {
    cy.nodes().addClass('nav-risk-high');
  }
}

export function clearNavigationOverlay(cy) {
  if (!cy) return;
  cy.nodes().removeClass(NAVIGATION_CLASSES.join(' '));
}

export function bindNavigationToggle(toggleElemId) {
  const toggleEl = document.getElementById(toggleElemId);
  if (!toggleEl) return;
  toggleEl.addEventListener('change', (e) => {
    if (window.cy) {
      clearNavigationOverlay(window.cy);
      if (e.target.checked) {
        applyNavigationOverlay(window.cy, window.__bridgeArtifacts?.navigation_state);
      }
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindNavigationToggle = bindNavigationToggle;
}
