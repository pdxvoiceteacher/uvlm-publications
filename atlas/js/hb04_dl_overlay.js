async function loadHB04() {
  const res = await fetch('/artifacts/hb04_dl_backtest.json', { cache: 'no-store' });
  const data = await res.json();

  const corridors = data.corridors || [];

  corridors.forEach((c) => {
    const node = window.cy?.getElementById(c.node_id);

    if (node && node.length) {
      node.addClass('hb04-corridor');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-hb04-dl');

  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadHB04);
});
