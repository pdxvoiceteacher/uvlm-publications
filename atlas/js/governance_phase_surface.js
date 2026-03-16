let surfaceLoaded = false;

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-phase-surface');

  if (!btn || btn.dataset.bound === 'true') {
    return;
  }

  btn.dataset.bound = 'true';

  btn.addEventListener('click', async () => {
    if (surfaceLoaded) return;

    const res = await fetch('/artifacts/governance_phase_diagram.json', { cache: 'no-store' });
    const data = await res.json();

    renderPhaseSurface(data.surface || []);

    surfaceLoaded = true;
  });
});

function renderPhaseSurface(points) {
  const container = document.getElementById('phase-surface-container');
  if (!container || !window.THREE) {
    return;
  }

  const width = Math.floor(window.innerWidth * 0.8);
  const height = 600;

  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);

  const renderer = new THREE.WebGLRenderer({ antialias: true });

  renderer.setSize(width, height);

  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  camera.position.set(2, 2, 3);
  camera.lookAt(0, 0, 0);

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(5, 5, 5);
  scene.add(light);

  const geometry = new THREE.BufferGeometry();

  const vertices = [];
  const colors = [];

  points.forEach((p) => {
    const x = Number(p?.psi ?? 0) - 0.5;
    const z = Number(p?.r_capture ?? 0) - 0.5;
    const y = Number(p?.omega ?? 0);

    vertices.push(x, y, z);

    const color = regimeColor(p?.regime);

    colors.push(color.r, color.g, color.b);
  });

  geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

  const material = new THREE.PointsMaterial({
    size: 0.03,
    vertexColors: true
  });

  const mesh = new THREE.Points(geometry, material);

  scene.add(mesh);

  const axesHelper = new THREE.AxesHelper(1.5);
  scene.add(axesHelper);

  function animate() {
    requestAnimationFrame(animate);

    mesh.rotation.y += 0.002;

    renderer.render(scene, camera);
  }

  animate();
}

function regimeColor(regime) {
  switch (regime) {
    case 'golden_age':
      return new THREE.Color(0x00ff88);

    case 'stable_discovery':
      return new THREE.Color(0x33aaff);

    case 'orthodoxy_drift':
      return new THREE.Color(0xffcc00);

    case 'fragmentation':
      return new THREE.Color(0xff8800);

    case 'civilizational_rupture':
      return new THREE.Color(0xff2222);

    default:
      return new THREE.Color(0xffffff);
  }
}
