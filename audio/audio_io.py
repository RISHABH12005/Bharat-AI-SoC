import os
import pyaudio
from audio.usb_mic import record_usb
from audio.inmp441_mic import record_inmp441


def find_usb_mic():
    pa = pyaudio.PyAudio()

    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)

        if info["maxInputChannels"] > 0:
            name = info["name"].lower()
            if any(k in name for k in ["usb", "mic", "microphone", "input"]):
                pa.terminate()
                return i

    pa.terminate()
    return None


def is_real_pi():
    """
    Detects whether code is running on real Raspberry Pi hardware.
    VM will usually fail this.
    """
    try:
        with open("/proc/cpuinfo") as f:
            return "Raspberry Pi" in f.read()
    except Exception:
        return False


def record_audio(duration=2.0):
    usb_index = find_usb_mic()

    # Priority 1: USB mic (works on VM + Pi)
    if usb_index is not None:
        print("[Audio] Using USB microphone")
        return record_usb(duration_sec=duration, device_index=usb_index)

    # Priority 2: INMP441 (ONLY on real Pi)
    if is_real_pi():
        print("[Audio] USB mic not found, using INMP441 (I2S)")
        return record_inmp441(duration_sec=duration)

    # VM-safe fallback
    print("[Audio] No microphone available (VM or WSL environment)")
    return None
