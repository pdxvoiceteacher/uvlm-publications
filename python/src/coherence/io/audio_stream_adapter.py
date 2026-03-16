"""Audio stream adapter for multimodal telemetry ingestion."""

from queue import Queue

import numpy as np
import sounddevice as sd


def ingest_audio_stream(samplerate=44100, channels=1, blocksize=1024):
    """Yield audio chunks captured from the default input stream."""
    chunks = Queue()

    def callback(indata, _frames, _time, _status):
        chunks.put(np.copy(indata))

    with sd.InputStream(
        callback=callback,
        samplerate=samplerate,
        channels=channels,
        blocksize=blocksize,
    ):
        while True:
            yield chunks.get()
