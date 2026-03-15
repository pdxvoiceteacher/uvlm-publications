let audioEl = null;

function highlightNodes() {
  const nodes = document.querySelectorAll('[data-node]');
  nodes.forEach((node) => node.classList.add('overlay-musical-coherence'));
}

function clearHighlightNodes() {
  const nodes = document.querySelectorAll('.overlay-musical-coherence');
  nodes.forEach((node) => node.classList.remove('overlay-musical-coherence'));
}

function stopAudio() {
  if (!audioEl) return;
  audioEl.pause();
  audioEl.currentTime = 0;
}

function playAudio() {
  if (!audioEl) {
    audioEl = new Audio('/artifacts/midi/coherence_stream.mid');
    audioEl.loop = true;
  }
  audioEl.play().catch(() => {
    // autoplay can be blocked; keep visual overlay active
  });
}

function toggleMusicalCoherence() {
  const active = Boolean(document.querySelector('.overlay-musical-coherence'));

  if (active) {
    clearHighlightNodes();
    stopAudio();
    return;
  }

  highlightNodes();
  playAudio();
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('toggle-musical-coherence');
  if (!btn || btn.dataset.bound === 'true') return;

  btn.dataset.bound = 'true';
  btn.addEventListener('click', toggleMusicalCoherence);
});
