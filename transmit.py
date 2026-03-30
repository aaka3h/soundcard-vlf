import pyaudio
import numpy as np
import argparse
import time

SAMPLE_RATE = 44100
FREQUENCY   = 15000
AMPLITUDE   = 0.9
CHUNK_SIZE  = 1024

def generate_chunk(frequency, sample_rate, chunk_size, amplitude, phase):
    t = (np.arange(chunk_size) + phase) / sample_rate
    samples = amplitude * np.sin(2 * np.pi * frequency * t)
    return samples.astype(np.float32), phase + chunk_size

def main():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True, frames_per_buffer=CHUNK_SIZE)
    print(f"Transmitting {FREQUENCY} Hz — press Ctrl+C to stop")
    phase = 0
    start = time.time()
    try:
        while True:
            chunk, phase = generate_chunk(FREQUENCY, SAMPLE_RATE, CHUNK_SIZE, AMPLITUDE, phase)
            stream.write(chunk.tobytes())
            print(f"\rTransmitting... {time.time()-start:.1f}s", end="", flush=True)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

if __name__ == "__main__":
    main()
