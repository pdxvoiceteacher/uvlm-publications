export async function loadTheoryMap() {
  const res = await fetch('/artifacts/theory_map.json');
  return await res.json();
}

export function applyTheoryOverlay(data) {
  console.log('Theories:', data.theories);
  console.log('Terraces:', data.terraces);
}
