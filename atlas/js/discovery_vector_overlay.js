let vectorFieldLoaded = false;

function vectorColor(conf) {
  if (conf > 0.8) return 0x00ff88;
  if (conf > 0.6) return 0x66ccff;
  if (conf > 0.4) return 0xffcc00;
  return 0xff4444;
}

function renderDiscoveryVectors(vectors) {
  if (!window.THREE) return;

  const scene = window.phaseSurfaceScene || window.atlasScene;
  if (!scene) return;

  const scale = 0.25;
  const arrows = [];

  vectors.forEach((v) => {
    const origin = new THREE.Vector3(
      Number(v?.x ?? 0) - 0.5,
      Number(v?.psi ?? 0),
      Number(v?.y ?? 0) - 0.5
    );

    const direction = new THREE.Vector3(
      Number(v?.dx ?? 0),
      Number(v?.dy ?? 0),
      Number(v?.dz ?? 0)
    );

    if (direction.lengthSq() === 0) {
      return;
    }

    direction.normalize();

    const length = Number(v?.magnitude ?? 0) * scale;
    const color = new THREE.Color(vectorColor(Number(v?.confidence ?? 0)));

    const arrow = new THREE.ArrowHelper(direction, origin, length, color);
    scene.add(arrow);
    arrows.push(arrow);
  });

  window.discoveryVectorArrows = arrows;
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-discovery-vectors');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', async () => {
    if (vectorFieldLoaded) return;

    const res = await fetch('/artifacts/discovery_vector_field.json', { cache: 'no-store' });
    const data = await res.json();

    renderDiscoveryVectors(Array.isArray(data?.vectors) ? data.vectors : []);

    vectorFieldLoaded = true;
  });
});
