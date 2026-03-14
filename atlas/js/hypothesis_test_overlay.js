export async function loadHypothesisTests() {
  const res = await fetch('/artifacts/hypothesis_test_map.json');
  return await res.json();
}

export function applyHypothesisTestOverlay(data) {
  console.log('Hypothesis test results:', data.summary);
}
