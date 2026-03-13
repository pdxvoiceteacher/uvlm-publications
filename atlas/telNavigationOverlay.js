const NAV_CLASSES = ['nav-psi-high', 'nav-risk-high'];

export const NAVIGATION_RESETTABLE_CLASSES = [...NAV_CLASSES];

function clearNavigationClasses(cy) {
  if (!cy) return;
  cy.nodes(`.${NAV_CLASSES.join(', .')}`).removeClass(NAV_CLASSES.join(' '));
}

function applyNodeHighlight(cy, nodeId, riskByNode = {}) {
  if (!nodeId) return;
  const node = cy.getElementById(nodeId);
  if (!node || node.empty()) return;

  node.addClass('nav-psi-high');
  if (Number(riskByNode[nodeId] ?? 0) > 0.8) {
    node.addClass('nav-risk-high');
  }
}

export function applyNavigationOverlay(cy, chosenState, riskByNode = {}) {
  if (!cy) return;
  clearNavigationClasses(cy);

  if (!chosenState) return;

  if (typeof chosenState === 'string') {
    applyNodeHighlight(cy, chosenState, riskByNode);
    return;
  }

  if (Array.isArray(chosenState)) {
    chosenState.forEach((nodeId) => applyNodeHighlight(cy, nodeId, riskByNode));
    return;
  }

  if (typeof chosenState === 'object') {
    Object.keys(chosenState).forEach((nodeId) => applyNodeHighlight(cy, nodeId, riskByNode));
  }
}

export function clearNavigationOverlay(cy) {
  clearNavigationClasses(cy);
}

export function bindNavigationToggle(toggleElemId) {
  const toggle = document.getElementById(toggleElemId);
  if (!toggle) return;

  toggle.addEventListener('change', () => {
    if (!window.cy) return;

    if (toggle.checked) {
      const navState = window.__bridgeArtifacts?.navigation_state || {};
      applyNavigationOverlay(window.cy, navState.chosen_state, navState.risk_by_node || {});
    } else {
      window.cy.nodes().removeClass(NAV_CLASSES.join(' '));
    }
  });
}

if (typeof window !== 'undefined') {
  window.bindNavigationToggle = bindNavigationToggle;
}
