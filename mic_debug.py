import pyaudio
import time

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')

print("Available audio input devices:")
for i in range(0, num_devices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print(f"  ID: {i} - {p.get_device_info_by_host_api_device_index(0, i).get('name')}")

# Try to open a stream and listen
try:
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)
    print("\nListening for 5 seconds... (Speak now!)")
    frames = []
    for _ in range(0, int(44100 / 1024 * 5)): # 5 seconds of audio
        data = stream.read(1024)
        frames.append(data)
    print("Finished listening.")
    stream.stop_stream()
    stream.close()
    print("Microphone appears to be working.")
except Exception as e:
    print(f"\nError accessing microphone: {e}")
finally:
    p.terminate()