async function loadAntiCapture() {
  const res = await fetch('/artifacts/anti_capture_diagnostics.json', {
    cache: 'no-store'
  });

  const data = await res.json();

  renderAntiCapturePanel(data);
}

function renderAntiCapturePanel(data) {
  let panel = document.getElementById('anti-capture-panel');

  if (!panel) {
    panel = document.createElement('div');
    panel.id = 'anti-capture-panel';
    panel.className = 'atlas-panel';
    document.body.appendChild(panel);
  }

  const riskScore = Number(data?.risk_score ?? 0);
  const regime = data?.regime ?? 'unknown';

  panel.innerHTML = `
    <h3>Governance Capture Risk</h3>
    <p>Regime: ${regime}</p>
    <p>Risk Score: ${riskScore.toFixed(3)}</p>
  `;
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-anti-capture');

  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadAntiCapture);
});
