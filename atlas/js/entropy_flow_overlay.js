export async function loadEntropyFlow() {
  const res = await fetch('/artifacts/entropy_flow_map.json', { cache: 'no-store' });
  if (!res.ok) return null;
  return await res.json();
}

export function applyEntropyFlowOverlay(data) {
  const nodes = Array.isArray(data?.nodes) ? data.nodes : [];
  nodes.forEach((node) => {
    const el = document.querySelector(`[data-node="${node.id}"]`);
    if (!el) return;
    if ((node.entropyGradient ?? 0) > 0) {
      el.classList.add('overlay-entropy-flow');
      el.setAttribute('data-entropy-gradient', `∇S=${Number(node.entropyGradient).toFixed(3)}`);
    }
  });
}

export function clearEntropyFlowOverlay() {
  document.querySelectorAll('.overlay-entropy-flow').forEach((el) => {
    el.classList.remove('overlay-entropy-flow');
    el.removeAttribute('data-entropy-gradient');
  });
}
