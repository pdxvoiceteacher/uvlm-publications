function renderKnowledgeEcosystemPanel(data) {
  const panel = document.getElementById('ecosystem-panel');
  if (!panel) return;

  panel.innerHTML = `
    Regime: ${data.regime}<br>
    Diversity: ${data.diversity}<br>
    Entropy: ${data.entropy}<br>
    Turnover: ${data.turnover_rate}
  `;
}

function loadKnowledgeEcosystem() {
  return fetch('/bridge/knowledge_ecosystem_map.json', { cache: 'no-store' })
    .then((r) => r.json())
    .then((data) => {
      renderKnowledgeEcosystemPanel(data);
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-knowledge-ecosystem');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', loadKnowledgeEcosystem);
});
