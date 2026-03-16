async function loadTheoryEvolutionMap() {
  const response = await fetch('/bridge/theory_evolution_map.json', { cache: 'no-store' });
  if (!response.ok) return null;
  return await response.json();
}

function clearTheoryEvolutionOverlay() {
  if (window.cy) {
    window.cy.nodes('.theory-evolution').removeClass('theory-evolution');
  }

  document.querySelectorAll('.theory-evolution').forEach((node) => {
    node.classList.remove('theory-evolution');
  });
}

function applyTheoryEvolutionOverlay(data) {
  const theories = Array.isArray(data?.theories) ? data.theories : [];

  theories.forEach((t) => {
    const theoryId = String(t?.id ?? '');
    if (!theoryId) return;

    if (window.cy) {
      const cyNode = window.cy.getElementById(theoryId);
      if (cyNode && cyNode.length) {
        cyNode.addClass('theory-evolution');
      }
    }

    const node = document.querySelector(`[data-theory="${theoryId}"]`) || document.getElementById(theoryId);
    if (node) {
      node.classList.add('theory-evolution');
    }
  });
}

async function toggleTheoryEvolution() {
  const hasOverlay = Boolean(
    (window.cy && window.cy.nodes('.theory-evolution').length > 0) ||
    document.querySelector('.theory-evolution')
  );

  if (hasOverlay) {
    clearTheoryEvolutionOverlay();
    return;
  }

  const data = await loadTheoryEvolutionMap();
  if (!data) return;

  applyTheoryEvolutionOverlay(data);
}

document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('toggle-theory-evolution');
  if (!button || button.dataset.bound === 'true') return;

  button.dataset.bound = 'true';
  button.addEventListener('click', toggleTheoryEvolution);
});
