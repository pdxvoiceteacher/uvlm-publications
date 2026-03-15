async function loadEvolutionState() {

  const res = await fetch('/artifacts/evolution_state.json', {
    cache: 'no-store'
  });

  return await res.json();
}


function renderEvolutionPanel(state) {

  const panel = document.getElementById('evolution-panel');

  panel.innerHTML = `
    <h3>Triadic Brain Evolution</h3>
    <p>Step: ${state.step}</p>
    <p>Hypotheses: ${state.hypotheses}</p>
    <p>Theories: ${state.theories}</p>
    <p>Paradigm Shifts: ${state.paradigm_shifts}</p>
    <p>Regime: ${state.civilizational_regime}</p>
  `;
}
