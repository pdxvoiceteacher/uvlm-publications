async function loadMidi() {

  const res = await fetch('/artifacts/coherence_stream.mid', {cache:'no-store'})

  const buffer = await res.arrayBuffer()

  const ctx = new AudioContext()

  const audio = new Audio('artifacts/coherence_stream.mid')

  audio.play()
}

document.getElementById('toggle-coherence-audio')
  .addEventListener('click', loadMidi)
