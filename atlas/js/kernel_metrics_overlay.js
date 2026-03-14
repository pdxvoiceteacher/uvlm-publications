async function loadKernelMetrics() {
  const response = await fetch('/artifacts/kernel_metrics.json');
  if (!response.ok) return null;
  return await response.json();
}

function renderKernelMetrics(metrics) {
  const panel = document.createElement('div');
  panel.className = 'kernel-metrics-panel';

  panel.innerHTML = `
    <h3>Kernel Metrics</h3>
    <p><b>Phi total:</b> ${metrics.phi_total.toFixed(4)}</p>
    <p><b>Phi drift:</b> ${metrics.phi_drift.toFixed(4)}</p>
    <p><b>Corridor residual:</b> ${metrics.corridor_mass_balance_residual.toFixed(6)}</p>
  `;

  return panel;
}

async function toggleKernelMetrics() {
  const existing = document.querySelector('.kernel-metrics-panel');

  if (existing) {
    existing.remove();
    return;
  }

  const metrics = await loadKernelMetrics();

  if (!metrics) return;

  const panel = renderKernelMetrics(metrics);
  document.body.appendChild(panel);
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-kernel-metrics');

  if (!btn) return;

  btn.addEventListener('click', toggleKernelMetrics);
});
