import math
import pyaudio
import matplotlib.pyplot as plt
import matplotlib.figure
import mpld3
from io import StringIO
import wave

import numpy as np
from PIL import Image

# WAVE PARAMETERS
DEFAULT_BIT_RATE = 16000
DEFAULT_FREQUENCY = 800
UNIT = 0.1  # BASE UNIT FOR SIGNAL SPEED
LENGTH_DOT = 1 * UNIT
LENGTH_DASH = 3 * UNIT


class Wave:

    def __init__(self, bit_rate=DEFAULT_BIT_RATE, freq=DEFAULT_FREQUENCY):
        self.Value = ''
        self.Bit_rate = bit_rate  # number of frames per second
        self.Frequency = freq  # Hz, waves per second

    # CONVERT A MORSE CODE INTO CHAR SIGNAL
    def morse_to_wave(self, word):
        for letter in word:
            if letter == '.':
                self.Value += wave_dot()
            elif letter == '-':
                self.Value += wave_dash()
            elif letter == ' ':
                for x in range(int(max(self.Bit_rate, self.Frequency + 100) * LENGTH_DOT)):
                    self.Value += chr(0)

    # CONVERT CHAR SIGNAL TO SOUND VIA PyAudio
    def generate_sound(self):

        # Instantiate PyAudio and initialize PortAudio system resources (1)
        PyAudio = pyaudio.PyAudio
        p = PyAudio()

        # Open stream (2)

        InMemory_Wav = StringIO(self.Value)  # Create an in-memory WAV file
        with wave.open(InMemory_Wav, 'rb') as wf:
            stream = p.open(format=wf.get_format_from_width(),
                        channels=1,
                        rate=self.Bit_rate,
                        output=True)

        #InMemory_Wav.seek(0)
        stream.read(0)
        stream.stop_stream()
        stream.close()
        wf.terminate()

        #audio_buffer.seek(0)  # Reset buffer position to the beginning
        #return audio_buffer


    # SHOW THE VALUE OF THE SIGNAL ON PLOT
    def show_sound(self):
        # Convert WAVEDATA to numerical values
        wave_values = [ord(char) for char in self.Value]

        # Plot the waveform
        plt.figure(figsize=(18, 4))
        fig = plt.plot(wave_values, color='blue')
        plt.title("Waveform Visualization of WAVEDATA")
        plt.xlabel("Sample Index")
        plt.ylabel("Amplitude (0 to 255)")

        # To write
        fig.set_canvas()
        image = mpld3.fig_to_html(fig)
        return image


# CREATE A SIGNAL
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
            WAVE += chr(0)

    for x in range(int(bit_rate * LENGTH_DOT)):
        WAVE += chr(0)
    return WAVE


def wave_dot():
    return generate_wave(DEFAULT_FREQUENCY, DEFAULT_BIT_RATE, LENGTH_DOT)


def wave_dash():
    return generate_wave(DEFAULT_FREQUENCY, DEFAULT_BIT_RATE, LENGTH_DASH)

def generate_sound(value, bit_rate):
    print(bit_rate)
    bit_rate = bit_rate  # Sample rate in Hz

    # Instantiate PyAudio and initialize PortAudio system resources (1)
    PyAudio = pyaudio.PyAudio
    p = PyAudio()

    # Open stream (2)
    # Create an in-memory WAV file
    audio_buffer = io.BytesIO()
    with p.open(format=p.get_format_from_width(1),
                channels=1,
                rate=bit_rate,
                output=True) as wf:
        wf.writeframes(value)  # use .tobytes() ?

    audio_buffer.seek(0)  # Reset buffer position to the beginning
    return audio_buffer.read()