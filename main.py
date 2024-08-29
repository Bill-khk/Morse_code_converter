import pandas as pd
import math
import pyaudio
import matplotlib.pyplot as plt

PyAudio = pyaudio.PyAudio  # initialize pyaudio

# ----------------- SIMPLE MORSE CONVERSION FUNCTION -----------------
df = pd.read_csv('morse.csv', names=['CHAR', 'MORSE'], header=None)
to_convert = "AUDIO"  # input('Enter a word : ').upper()
converted = ""

for letter in to_convert:
    converted += df.MORSE[df.CHAR == letter].values[0]
    converted += " "

print(converted)

# ----------------- GENERATING SOUND -----------------
# Creating audio, based on this https://stackoverflow.com/a/33880295/26414904

# Wave parameters
BITRATE = 16000  # number of frames per second
FREQUENCY = 800  # Hz, waves per second
LENGTH = 0.1

def generate_wave(freq, bit_rate, sample_length, fill=False):
    WAVE = ''
    bit_rate = max(bit_rate, freq + 100)
    nb_frames = int(bit_rate * sample_length)
    # Generate wave
    for x in range(nb_frames):
        WAVE += chr(int(math.sin(x / ((bit_rate / freq) / math.pi)) * 127 + 128))

    if fill:
        rest_frames = nb_frames % bit_rate
        for x in range(rest_frames):
            WAVE += chr(128)
    return WAVE
def generate_sound(sound):
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1),
                    channels=1,
                    rate=BITRATE,
                    output=True)

    stream.write(sound)
    stream.stop_stream()
    stream.close()
    p.terminate()

# VISUALISE THE SOUND INTO CHART
def show_sound(sound):
    # Convert WAVEDATA to numerical values
    wave_values = [ord(char) for char in sound]

    # Plot the waveform
    plt.figure(figsize=(10, 4))
    plt.plot(wave_values, color='blue')
    plt.title("Waveform Visualization of WAVEDATA")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude (0 to 255)")
    plt.show()

# -----------------MAIN------------------------
WAVEDATA = generate_wave(FREQUENCY, BITRATE, LENGTH, True)
generate_sound(WAVEDATA)
show_sound(WAVEDATA)