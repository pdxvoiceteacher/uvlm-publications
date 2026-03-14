export async function loadTerraceArtifact() {
  const res = await fetch('/artifacts/terrace_formation_map.json');
  return await res.json();
}

export function applyTerraceOverlay(artifact) {
  console.log('Terrace density overlay:', artifact.summary);
}
