# Soundcard VLF Experiment

A small Python experiment that generates a 15 kHz audio tone and plots an RTL-SDR spectrum near the same frequency. It is intended for investigating possible coupling between an audio cable and a nearby receiver.

The scripts alone do not establish a calibrated transmission range or prove that a received peak is radiated VLF energy. A peak may also result from local interference, coupling, or a receiver configuration problem.

## Scripts

| File | Behavior |
| --- | --- |
| [transmit.py](transmit.py) | Plays a continuous 15,000 Hz sine wave through the default audio output using PyAudio. Defaults: 44,100 samples/s, mono float32, amplitude 0.9. |
| [receive.py](receive.py) | Reads RTL-SDR samples and displays a Matplotlib FFT plot from 10 to 20 kHz, with a marker at 15 kHz. Defaults: 250,000 samples/s and a 4,096-point FFT. |

Despite its name, `transmit.py` is an audio tone generator. The receiver is a separate experiment; the scripts do not exchange or decode messages.

## Receiver compatibility

The current receiver calls `set_direct_sampling(2)` and sets the center frequency to 24 MHz. Its graph uses FFT bin frequencies without adding that center frequency.

**This is not a validated RTL-SDR Blog V4 configuration.** The manufacturer's [V4 user guide](https://www.rtl-sdr.com/v4/) states that enabling direct sampling on a V4 produces no results. The [V4 datasheet](https://www.rtl-sdr.com/wp-content/uploads/2024/12/RTLSDR_V4_Datasheet_V_1_0.pdf) specifies a lower tuning limit of 500 kHz, above the experiment's 15 kHz target. Validating VLF reception requires a suitable receiving path and corresponding software configuration.

The FFT values are calculated as `20 * log10(abs(FFT) + 1e-12)` without normalization or calibration. Although the plot labels them “dBFS,” they are relative FFT magnitudes and should not be reported as calibrated dBFS, signal power, or SNR. The previous “145 dBFS above noise floor” claim is not supported by this calculation.

## Setup

Requirements:

- Python 3, Git, and an audio output that supports 44.1 kHz playback.
- PyAudio, NumPy, Matplotlib, and pyrtlsdr.
- PortAudio for audio playback and the appropriate native RTL-SDR library/USB drivers for receiver access.
- A graphical desktop for the Matplotlib receiver window.

Use a virtual environment on Linux or macOS:

```bash
git clone https://github.com/aaka3h/soundcard-vlf.git
cd soundcard-vlf
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pyaudio numpy matplotlib pyrtlsdr
```

If PyAudio needs to build from source, install PortAudio and Python development headers first; see the [PyAudio installation guide](https://people.csail.mit.edu/hubert/pyaudio/). Installing `pyrtlsdr` does not by itself install or configure the native receiver driver.

On Windows, create the environment with `py -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1` in PowerShell, then run the same pip command.

## Run the experiment

Select the intended output device in your operating system before starting. The script uses the default output and has no device-selection or frequency command-line options. Start with low system volume; the source amplitude is 0.9.

In the first terminal, with the environment active:

```bash
python transmit.py
```

For receiver experiments, review the compatibility limitations above before running this in a second terminal with the same environment active:

```bash
python receive.py
```

Stop the tone generator with **Ctrl+C**. Close the plot window to stop the receiver and release the SDR.

Change `FREQUENCY` in `transmit.py` and the receiver's target and plot ranges in `receive.py` to investigate other frequencies; there are no implemented command-line settings.

## Interpreting observations

Compare tone-on and tone-off measurements, vary the tone frequency, and document the receiver model, driver, signal path, gain, FFT settings, cable arrangement, and distance. A repeatable peak that follows the tone is an observation to investigate; identifying the coupling mechanism requires additional controls.

No measurement captures or calibration data are included in this repository.

## Author

Aakash — [@aaka3h](https://github.com/aaka3h).
