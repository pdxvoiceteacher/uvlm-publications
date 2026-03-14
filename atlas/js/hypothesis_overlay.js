export async function loadHypotheses() {
  const res = await fetch('/artifacts/hypothesis_map.json');
  return await res.json();
}

export function applyHypothesisOverlay(artifact) {
  console.log('Candidate hypotheses:', artifact.summary);
}
