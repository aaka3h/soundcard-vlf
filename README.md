# 📡 Soundcard VLF Experiment

> Using a laptop soundcard as a VLF transmitter and RTL-SDR V4 as a receiver.

## What This Is

This experiment proves that a standard laptop headphone jack can radiate a detectable electromagnetic signal at **15 kHz (VLF band)** using nothing but headphones and a Python script.

The headphone cable itself acts as the transmitting antenna while simultaneously playing audio — no hardware modification required.

## How It Works
```
transmit.py → headphone jack → cable radiates EM at 15 kHz
                                        ↓
                              RTL-SDR V4 (direct sampling mode)
                                        ↓
                              receive.py → live FFT spike at 15 kHz
```

## Results

- Signal peaked at **145 dBFS** above noise floor
- RTL-SDR V4 picked up signal within ~1 meter range
- Headphone cable confirmed as accidental VLF antenna

## Hardware Used

| Item | Role |
|---|---|
| Laptop headphone jack | Transmitter |
| Headphone cable | Antenna |
| RTL-SDR V4 dongle | Receiver |

## Run It
```bash
# Install dependencies
sudo apt install python3-pyaudio rtl-sdr librtlsdr-dev
pip3 install numpy matplotlib pyrtlsdr --break-system-packages

# Terminal 1
python3 transmit.py

# Terminal 2
python3 receive.py
```

## Author

**Aakash** — ham radio operator, SDR enthusiast, self-taught developer.
