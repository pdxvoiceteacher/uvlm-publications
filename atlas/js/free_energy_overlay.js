export async function loadFreeEnergy() {
  const res = await fetch('/artifacts/free_energy_map.json', { cache: 'no-store' });
  if (!res.ok) return null;
  return await res.json();
}

export function applyFreeEnergyOverlay(data) {
  const summary = data?.summary ?? {};
  console.log('Free energy overlay:', {
    freeEnergyMin: summary.freeEnergyMin,
    freeEnergyMax: summary.freeEnergyMax,
    discoveryTemperature: summary.discoveryTemperature,
  });

  const nodes = Array.isArray(data?.nodes) ? data.nodes : [];
  nodes.forEach((node) => {
    const el = document.querySelector(`[data-node="${node.id}"]`);
    if (!el) return;
    if (Number.isFinite(node.freeEnergy)) {
      el.classList.add('overlay-free-energy');
      el.setAttribute('data-free-energy', `F=${Number(node.freeEnergy).toFixed(3)}`);
    }
  });
}

export function clearFreeEnergyOverlay() {
  document.querySelectorAll('.overlay-free-energy').forEach((el) => {
    el.classList.remove('overlay-free-energy');
    el.removeAttribute('data-free-energy');
  });
}
