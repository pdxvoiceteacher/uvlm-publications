function setBacktestOverlayPanel(html) {
  const panel = document.getElementById('backtest-overlay-panel');
  if (!panel) return;
  panel.innerHTML = html;
}

function clearBacktestOverlay() {
  if (window.cy) {
    window.cy.nodes('.backtest-detected-corridor').removeClass('backtest-detected-corridor');
    window.cy.nodes('.backtest-true-breakthrough').removeClass('backtest-true-breakthrough');
    window.cy.nodes('.backtest-false-positive').removeClass('backtest-false-positive');
  }

  document.querySelectorAll('.backtest-detected-corridor, .backtest-true-breakthrough, .backtest-false-positive').forEach((node) => {
    node.classList.remove('backtest-detected-corridor', 'backtest-true-breakthrough', 'backtest-false-positive');
  });

  setBacktestOverlayPanel('Backtest overlay is inactive.');
}

function applyNodeClass(nodeId, className) {
  if (window.cy) {
    const cyNode = window.cy.getElementById(String(nodeId));
    if (cyNode && cyNode.length) cyNode.addClass(className);
  }

  const domNode = document.getElementById(String(nodeId));
  if (domNode) domNode.classList.add(className);
}

function listFromDataset(dataset, keyA, keyB) {
  if (Array.isArray(dataset?.[keyA])) return dataset[keyA];
  if (Array.isArray(dataset?.[keyB])) return dataset[keyB];
  return [];
}

function applyBacktestOverlay(datasetName, dataset) {
  const detectedCorridors = listFromDataset(dataset, 'detected_corridors', 'corridors');
  const trueBreakthroughs = listFromDataset(dataset, 'true_breakthroughs', 'terraces');
  const falsePositives = listFromDataset(dataset, 'false_positives', 'falsePositive');

  detectedCorridors.forEach((nodeId) => applyNodeClass(nodeId, 'backtest-detected-corridor'));
  trueBreakthroughs.forEach((nodeId) => applyNodeClass(nodeId, 'backtest-true-breakthrough'));
  falsePositives.forEach((nodeId) => applyNodeClass(nodeId, 'backtest-false-positive'));

  setBacktestOverlayPanel(
    `<b>Scenario:</b> ${datasetName}<br>` +
    `• detected corridors: ${detectedCorridors.length}<br>` +
    `• true breakthroughs: ${trueBreakthroughs.length}<br>` +
    `• false positives: ${falsePositives.length}`
  );
}

function toggleBacktestOverlay() {
  const hasOverlay = Boolean(
    (window.cy && window.cy.nodes('.backtest-detected-corridor, .backtest-true-breakthrough, .backtest-false-positive').length > 0) ||
    document.querySelector('.backtest-detected-corridor, .backtest-true-breakthrough, .backtest-false-positive')
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
        setBacktestOverlayPanel('No backtest scenarios found.');
        return;
      }

      applyBacktestOverlay(scenarioName, data[scenarioName]);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-backtest-overlay');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', toggleBacktestOverlay);
});
