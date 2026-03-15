async function loadCoherenceGradientMap() {
  const res = await fetch('/artifacts/coherence_gradient_map.json', {
    cache: 'no-store',
  });
  if (!res.ok) return null;
  return await res.json();
}

function clearCoherenceGradientOverlay() {
  document.querySelectorAll('.overlay-coherence-gradient').forEach((el) => {
    el.classList.remove('overlay-coherence-gradient');
    el.removeAttribute('data-gradient');
  });
}

function applyCoherenceGradientOverlay(data) {
  const nodes = Array.isArray(data.nodes) ? data.nodes : [];
  nodes.forEach((node) => {
    const el = document.getElementById(node.id);
    if (!el) return;

    if ((node.gradientMagnitude || 0) > 0.05) {
      el.classList.add('overlay-coherence-gradient');
      el.setAttribute(
        'data-gradient',
        `|∇Φ|=${Number(node.gradientMagnitude).toFixed(3)} → ${node.bestNeighbor ?? 'n/a'}`
      );
    }
  });
}

async function toggleCoherenceGradientOverlay() {
  const existing = document.querySelector('.overlay-coherence-gradient');
  if (existing) {
    clearCoherenceGradientOverlay();
    return;
  }

  const data = await loadCoherenceGradientMap();
  if (!data) return;

  applyCoherenceGradientOverlay(data);
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-coherence-gradient');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', toggleCoherenceGradientOverlay);
});
