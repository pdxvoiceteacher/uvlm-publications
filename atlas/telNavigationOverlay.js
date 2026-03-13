// Atlas (Publisher) - Navigation Overlay

export const NAVIGATION_CLASSES = ['nav-psi-high', 'nav-risk-high'];
export const NAVIGATION_RESETTABLE_CLASSES = [...NAVIGATION_CLASSES];

export function clearNavigationOverlay(cy) {
  if (!cy) return;
  cy.nodes().removeClass(NAVIGATION_CLASSES.join(' '));
}

export function applyNavigationOverlay(cy, chosenState, riskMap) {
  if (!cy) return;
  clearNavigationOverlay(cy);
  if (!chosenState) return;

  const nodeId = Array.isArray(chosenState) ? chosenState[0] : chosenState;
  const element = cy.nodes(`[id="${nodeId}"]`);
  element.addClass('nav-psi-high');
  if (riskMap && riskMap[nodeId] > 1.0) {
    element.addClass('nav-risk-high');
  }
}

export function bindNavigationOverlayToggle(toggleId) {
  const toggle = document.getElementById(toggleId);
  if (!toggle) return;

  toggle.addEventListener('change', (e) => {
    if (e.target.checked) {
      const navState = window.__bridgeArtifacts?.navigation_state;
      const chosen = navState?.chosen_state;
      const riskMap = navState?.risk_by_node;
      applyNavigationOverlay(window.cy, chosen, riskMap);
    } else {
      clearNavigationOverlay(window.cy);
    }
  });
}

// Backward-compatible alias
export const bindNavigationToggle = bindNavigationOverlayToggle;

if (typeof window !== 'undefined') {
  window.bindNavigationOverlayToggle = bindNavigationOverlayToggle;
  window.bindNavigationToggle = bindNavigationToggle;
}
