async function runHB01() {
  const status = document.getElementById('experiment-status');

  const res = await fetch('/artifacts/hb01_relativity_backtest.json', { cache: 'no-store' });
  const data = await res.json();
  const corridors = Array.isArray(data?.corridors) ? data.corridors : [];

  if (status) {
    status.innerText = `HB-01 completed. Corridors detected: ${corridors.length}`;
  }
}

async function showConfidence() {
  const res = await fetch('/artifacts/corridor_confidence_calibrated.json', { cache: 'no-store' });
  const data = await res.json();

  const panel = document.getElementById('confidence-panel');
  if (!panel) {
    return;
  }

  panel.innerHTML = '';

  const corridors = Array.isArray(data?.corridors) ? data.corridors : [];

  corridors.forEach((c) => {
    const div = document.createElement('div');
    const topic = c?.topic ?? 'unknown-topic';
    const confidence = Number(c?.confidence ?? 0);
    div.innerText = `${topic} confidence: ${confidence.toFixed(3)}`;
    panel.appendChild(div);
  });
}

async function playCoherenceMusic() {
  const midi = await fetch('/artifacts/coherence_music.mid');
  const audio = new Audio(URL.createObjectURL(await midi.blob()));
  await audio.play();
}

async function toggleCorridors() {
  const res = await fetch('/artifacts/corridor_map.json', { cache: 'no-store' });
  const data = await res.json();

  const corridors = Array.isArray(data?.corridors) ? data.corridors : [];

  corridors.forEach((c) => {
    const node = window.cy?.getElementById(c.node_id);

    if (node && node.length) {
      node.addClass('corridor-highlight');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const runBtn = document.getElementById('run-hb01');
  const confidenceBtn = document.getElementById('toggle-confidence');
  const musicBtn = document.getElementById('play-coherence-music');
  const corridorBtn = document.getElementById('toggle-corridors');

  if (runBtn) runBtn.onclick = runHB01;
  if (confidenceBtn) confidenceBtn.onclick = showConfidence;
  if (musicBtn) musicBtn.onclick = playCoherenceMusic;
  if (corridorBtn) corridorBtn.onclick = toggleCorridors;
});
