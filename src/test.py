import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="output.wav", duration=5, fs=44100):
    print(f"Recording started for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, fs, recording)
    print(f"Recording saved as {filename}")

if __name__ == "__main__":
    duration = int(input("Enter duration in seconds: "))
    record_audio(duration=duration)
