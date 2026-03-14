async function loadDiscoveryCorridors() {
  const res = await fetch('/artifacts/discovery_corridors.json');

  if (!res.ok) return null;

  return await res.json();
}

function renderCorridors(data) {
  data.nodes.forEach((n) => {
    const el = document.getElementById(n.id);
    if (!el) return;

    if (n.psi_gradient > 0.05) {
      el.classList.add('overlay-corridor');
    }
  });
}

async function toggleCorridors() {
  const data = await loadDiscoveryCorridors();

  if (!data) return;

  renderCorridors(data);
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-corridors');
  if (!btn) return;

  btn.addEventListener('click', toggleCorridors);
});
