export async function loadConservationArtifact() {
  const res = await fetch('/artifacts/conservation_witness.json');
  return await res.json();
}

export function applyConservationOverlay(witnesses = []) {
  witnesses.forEach((witness) => {
    if (!witness?.within_tolerance) {
      console.warn('Conservation drift:', witness?.law_name);
    }
  });
}

export function bindConservationToggle(buttonId = 'toggle-conservation') {
  const btn = document.getElementById(buttonId);
  if (!btn || btn.dataset.boundConservationToggle === '1') {
    return;
  }

  btn.dataset.boundConservationToggle = '1';
  btn.addEventListener('click', async () => {
    const data = await loadConservationArtifact();
    applyConservationOverlay(data?.witnesses ?? []);
  });
}
