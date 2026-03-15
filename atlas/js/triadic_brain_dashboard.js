let simulationRunning = false;

async function startSimulation() {
  simulationRunning = true;

  const res = await fetch('/artifacts/civilizational_coherence_map.json', { cache: 'no-store' });
  const data = await res.json();

  console.log('Simulation Started:', data);
}

function pauseSimulation() {
  simulationRunning = false;
  console.log('Simulation paused');
}

async function toggleCorridors() {
  const res = await fetch('/artifacts/corridor_map.json', { cache: 'no-store' });
  const data = await res.json();

  console.log('Corridor vectors:', data);
}

async function toggleRenormalization() {
  const res = await fetch('/artifacts/renormalization_map.json', { cache: 'no-store' });
  const data = await res.json();

  console.log('Renormalization flow:', data);
}

async function playCoherenceAudio() {
  await fetch('/artifacts/coherence_music.mid');
  console.log('MIDI artifact loaded');
}

document.getElementById('start-simulation')
  .addEventListener('click', startSimulation);

document.getElementById('pause-simulation')
  .addEventListener('click', pauseSimulation);

document.getElementById('toggle-corridors')
  .addEventListener('click', toggleCorridors);

document.getElementById('toggle-renorm')
  .addEventListener('click', toggleRenormalization);

document.getElementById('play-coherence-audio')
  .addEventListener('click', playCoherenceAudio);
