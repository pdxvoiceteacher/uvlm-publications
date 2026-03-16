async function loadHB01() {
  const res = await fetch('/artifacts/hb01_relativity_backtest.json', { cache: 'no-store' });
  const data = await res.json();

  const corridors = data.corridors || [];

  corridors.forEach((c) => {
    const node = window.cy?.getElementById(c.node_id);

    if (node && node.length) {
      node.addClass('hb01-corridor');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-hb01-relativity');

  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadHB01);
});
