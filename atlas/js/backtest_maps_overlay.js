function setBacktestPanel(message) {
  const panel = document.getElementById('backtest-panel');
  if (!panel) return;
  panel.innerHTML = message;
}

function clearBacktestOverlay() {
  if (window.cy) {
    window.cy.nodes('.backtest-corridor').removeClass('backtest-corridor');
    window.cy.nodes('.backtest-river').removeClass('backtest-river');
    window.cy.nodes('.backtest-terrace').removeClass('backtest-terrace');
  }

  document.querySelectorAll('.backtest-corridor, .backtest-river, .backtest-terrace').forEach((node) => {
    node.classList.remove('backtest-corridor', 'backtest-river', 'backtest-terrace');
  });

  setBacktestPanel('Backtest map overlay is inactive.');
}

function applyNodeClass(nodeId, className) {
  if (window.cy) {
    const cyNode = window.cy.getElementById(String(nodeId));
    if (cyNode && cyNode.length) cyNode.addClass(className);
  }

  const domNode = document.getElementById(String(nodeId));
  if (domNode) domNode.classList.add(className);
}

function applyBacktestOverlay(datasetName, dataset) {
  const corridors = Array.isArray(dataset?.corridors) ? dataset.corridors : [];
  const rivers = Array.isArray(dataset?.rivers) ? dataset.rivers : [];
  const terraces = Array.isArray(dataset?.terraces) ? dataset.terraces : [];

  corridors.forEach((nodeId) => applyNodeClass(nodeId, 'backtest-corridor'));
  rivers.forEach((nodeId) => applyNodeClass(nodeId, 'backtest-river'));
  terraces.forEach((nodeId) => applyNodeClass(nodeId, 'backtest-terrace'));

  setBacktestPanel(
    `<b>Scenario:</b> ${datasetName}<br>` +
    `<b>Corridors:</b> ${corridors.length}<br>` +
    `<b>Rivers:</b> ${rivers.length}<br>` +
    `<b>Terraces:</b> ${terraces.length}`
  );
}

function toggleBacktestMap() {
  const hasOverlay = Boolean(
    (window.cy && window.cy.nodes('.backtest-corridor, .backtest-river, .backtest-terrace').length > 0) ||
    document.querySelector('.backtest-corridor, .backtest-river, .backtest-terrace')
  );

  if (hasOverlay) {
    clearBacktestOverlay();
    return;
  }

  fetch('/bridge/backtest_maps.json', { cache: 'no-store' })
    .then((r) => r.json())
    .then((data) => {
      const scenarioName = data.physics_1900_1950 ? 'physics_1900_1950' : Object.keys(data)[0];
      if (!scenarioName) {
        setBacktestPanel('No backtest scenarios found.');
        return;
      }

      applyBacktestOverlay(scenarioName, data[scenarioName]);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-backtest-map');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', toggleBacktestMap);
});
