export function bindTimelineControls({
  engine,
  modeEl,
  playEl,
  pauseEl,
  resetEl,
  speedEl,
  sliderEl,
  dateLabelEl,
  maxIndex
}) {
  sliderEl.min = '0';
  sliderEl.max = String(Math.max(0, maxIndex));
  sliderEl.step = '1';

  modeEl.addEventListener('change', () => engine.setMode(modeEl.value));
  playEl.addEventListener('click', () => engine.play());
  pauseEl.addEventListener('click', () => engine.pause());
  resetEl.addEventListener('click', () => engine.reset());
  speedEl.addEventListener('change', () => engine.setSpeed(speedEl.value));

  sliderEl.addEventListener('input', () => {
    engine.seekToIndex(Number(sliderEl.value));
  });

  engine.onStateChange((state) => {
    modeEl.value = state.mode;
    sliderEl.value = String(state.currentIndex);
    dateLabelEl.textContent = state.currentDate;
    speedEl.value = state.speedKey;

    const temporal = state.mode === 'temporal';
    playEl.disabled = !temporal || state.isPlaying;
    pauseEl.disabled = !temporal || !state.isPlaying;
    resetEl.disabled = !temporal;
    speedEl.disabled = !temporal;
    sliderEl.disabled = !temporal;
  });
}
