let relativityLoaded = false;

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-relativity-corridor');

  if (!btn || btn.dataset.bound === 'true') {
    return;
  }

  btn.dataset.bound = 'true';

  btn.addEventListener('click', async () => {
    if (relativityLoaded) return;

    const res = await fetch('/artifacts/relativity_corridor_map.json', { cache: 'no-store' });
    const data = await res.json();

    renderRelativityCorridor(data);

    relativityLoaded = true;
  });
});

function renderRelativityCorridor(data) {
  if (!window.THREE) return;

  const scene = window.atlasScene || window.phaseSurfaceScene;
  if (!scene) return;

  const nodes = Array.isArray(data?.nodes) ? data.nodes : [];
  const vectors = Array.isArray(data?.vectors) ? data.vectors : [];

  nodes.forEach((n) => {
    const sphere = new THREE.Mesh(
      new THREE.SphereGeometry(0.015),
      new THREE.MeshBasicMaterial({ color: 0xffcc00 })
    );

    sphere.position.set(Number(n?.x ?? 0) - 0.5, Number(n?.psi ?? 0), Number(n?.y ?? 0) - 0.5);

    scene.add(sphere);
  });

  vectors.forEach((v) => {
    const dir = new THREE.Vector3(
      Number(v?.dx ?? 0),
      Number(v?.dy ?? 0),
      Number(v?.dz ?? 0)
    );

    if (dir.lengthSq() === 0) {
      return;
    }

    dir.normalize();

    const origin = new THREE.Vector3(
      Number(v?.x ?? 0) - 0.5,
      Number(v?.psi ?? 0),
      Number(v?.y ?? 0) - 0.5
    );

    const arrow = new THREE.ArrowHelper(
      dir,
      origin,
      Number(v?.magnitude ?? 0) * 0.25,
      0x00ff88
    );

    scene.add(arrow);
  });
}
