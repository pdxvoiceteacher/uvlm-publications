const NAV_CLASSES = {
  psiHigh: 'nav-psi-high',
  riskHigh: 'nav-risk-high'
};

export const NAVIGATION_RESETTABLE_CLASSES = [NAV_CLASSES.psiHigh, NAV_CLASSES.riskHigh];

function isRiskHigh(nodeId, state = {}) {
  if (Array.isArray(state.governance_risk_high)) {
    return state.governance_risk_high.includes(nodeId);
  }

  const score = Number(state.risk_by_node?.[nodeId] ?? state.chosen_state_risk?.[nodeId] ?? 0);
  return score >= 0.8;
}

export function applyNavigationOverlay(cy, state = {}) {
  if (!cy) return;

  const chosenState = state.chosen_state || {};
  Object.entries(chosenState).forEach(([nodeId]) => {
    const node = cy.getElementById(nodeId);
    if (!node || node.empty()) return;

    node.addClass(NAV_CLASSES.psiHigh);
    if (isRiskHigh(nodeId, state)) {
      node.addClass(NAV_CLASSES.riskHigh);
    }
  });
}

export function clearNavigationOverlay(cy) {
  if (!cy) return;
  cy.elements().removeClass(`${NAV_CLASSES.psiHigh} ${NAV_CLASSES.riskHigh}`);
}

export function bindNavigationToggle(toggleElemId) {
  const toggleElem = document.getElementById(toggleElemId);
  if (!toggleElem) return;

  toggleElem.addEventListener('change', (e) => {
    const cy = window.cy;
    if (!cy) return;

    if (e.target.checked) {
      const navState = window.__bridgeArtifacts?.navigation_state || {};
      clearNavigationOverlay(cy);
      applyNavigationOverlay(cy, navState);
    } else {
      clearNavigationOverlay(cy);
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindNavigationToggle = bindNavigationToggle;
}
