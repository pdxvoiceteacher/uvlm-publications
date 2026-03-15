export async function loadParadigmShift() {
  const res = await fetch('/artifacts/paradigm_shift_map.json');
  return await res.json();
}

export function applyParadigmShiftOverlay(data) {
  console.log('Ruptures:', data.ruptures);
  console.log('New corridors:', data.new_corridors);
}
