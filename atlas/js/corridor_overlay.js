export async function loadCorridorArtifact() {
  const res = await fetch('/artifacts/corridor_map.json');
  return await res.json();
}

export function applyCorridorOverlay(artifact) {
  console.log('Discovery corridors:', artifact.summary);
}
