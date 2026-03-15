async function loadHB03() {
  const res = await fetch('/artifacts/hb03_quantum_backtest.json', { cache: 'no-store' });
  const data = await res.json();

  const corridors = data.corridors || [];

  corridors.forEach((c) => {
    const node = window.cy?.getElementById(c.node_id);

    if (node && node.length) {
      node.addClass('hb03-corridor');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-hb03-quantum');

  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadHB03);
});
