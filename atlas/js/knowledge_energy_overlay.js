export async function loadKnowledgeEnergy() {
  const res = await fetch('/artifacts/knowledge_energy_map.json', { cache: 'no-store' });
  if (!res.ok) return null;
  return await res.json();
}

export function applyKnowledgeEnergyOverlay(data) {
  const nodes = Array.isArray(data?.nodes) ? data.nodes : [];
  nodes.forEach((node) => {
    const el = document.querySelector(`[data-node="${node.id}"]`);
    if (!el) return;
    if ((node.energy ?? 0) > 0) {
      el.classList.add('overlay-knowledge-energy');
      el.setAttribute('data-energy', `E=${Number(node.energy).toFixed(3)}`);
    }
  });
}

export function clearKnowledgeEnergyOverlay() {
  document.querySelectorAll('.overlay-knowledge-energy').forEach((el) => {
    el.classList.remove('overlay-knowledge-energy');
    el.removeAttribute('data-energy');
  });
}
