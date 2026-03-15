export async function loadRiverArtifact() {
  const res = await fetch('/artifacts/river_formation_map.json');
  return await res.json();
}

export function applyRiverOverlay(artifact) {
  console.log('River formation:', artifact.summary);
}
