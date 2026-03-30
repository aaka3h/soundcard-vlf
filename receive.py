import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rtlsdr import RtlSdr

TARGET_FREQ = 15000
SAMPLE_RATE = 250000
GAIN        = 49.6
FFT_SIZE    = 4096

sdr = RtlSdr()
sdr.sample_rate = SAMPLE_RATE
sdr.center_freq = 24_000_000
sdr.gain = GAIN
sdr.set_direct_sampling(2)
print("RTL-SDR ready. Opening FFT window...")

fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor("#0d0d0d")
ax.set_facecolor("#0d0d0d")
line, = ax.plot([], [], color="#00ff88", lw=1)
ax.axvline(TARGET_FREQ/1e3, color="#ff4444", lw=1.5, linestyle="--", label=f"Target: {TARGET_FREQ/1e3} kHz")
ax.set_xlim(10, 20)
ax.set_ylim(-80, 20)
ax.set_xlabel("Frequency (kHz)", color="white")
ax.set_ylabel("Power (dBFS)", color="white")
ax.set_title("VLF Receiver — 15 kHz", color="white")
ax.tick_params(colors="white")
ax.grid(True, color="#222222")
ax.legend(facecolor="#1a1a1a", labelcolor="white")
peak_text = ax.text(0.02, 0.92, "", transform=ax.transAxes, color="#ffdd00", fontsize=10)

def update(_):
    samples = sdr.read_samples(FFT_SIZE * 4)
    windowed = samples[:FFT_SIZE] * np.hanning(FFT_SIZE)
    spectrum = np.fft.fftshift(np.fft.fft(windowed, FFT_SIZE))
    freqs = np.fft.fftshift(np.fft.fftfreq(FFT_SIZE, d=1/SAMPLE_RATE))
    power_db = 20 * np.log10(np.abs(spectrum) + 1e-12)
    mask = (freqs >= 10000) & (freqs <= 20000)
    line.set_data(freqs[mask]/1e3, power_db[mask])
    tmask = (freqs >= 14000) & (freqs <= 16000)
    if tmask.any():
        peak_text.set_text(f"Peak @ 15kHz: {power_db[tmask].max():.1f} dBFS")
    return line, peak_text

ani = animation.FuncAnimation(fig, update, interval=100, blit=True, cache_frame_data=False)
plt.tight_layout()
try:
    plt.show()
finally:
    sdr.close()
