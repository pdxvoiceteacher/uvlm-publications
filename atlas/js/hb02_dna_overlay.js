async function loadHB02() {
  const res = await fetch('/artifacts/hb02_dna_backtest.json', { cache: 'no-store' });
  const data = await res.json();

  const corridors = data.corridors || [];

  corridors.forEach((c) => {
    const node = window.cy?.getElementById(c.node_id);

    if (node && node.length) {
      node.addClass('hb02-corridor');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-hb02-dna');

  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadHB02);
});
