import math
import pyaudio
import matplotlib.pyplot as plt
import matplotlib.figure
import mpld3
from io import StringIO, BytesIO
import wave
import pyperclip

import numpy as np
from PIL import Image

# signal PARAMETERS
DEFAULT_BIT_RATE = 16000
DEFAULT_FREQUENCY = 800
UNIT = 0.1  # BASE UNIT FOR SIGNAL SPEED
LENGTH_DOT = 1 * UNIT
LENGTH_DASH = 3 * UNIT


class Signal:

    def __init__(self, bit_rate=DEFAULT_BIT_RATE, freq=DEFAULT_FREQUENCY):
        self.Value = ''
        self.Bit_rate = bit_rate  # number of frames per second
        self.Frequency = freq  # Hz, signals per second

    # CONVERT A MORSE CODE INTO CHAR SIGNAL
    def morse_to_signal(self, word):
        self.Value = ""  # Flushing the value since using global WAVEDATA
        for letter in word:
            if letter == '.':
                self.Value += signal_dot()
            elif letter == '-':
                self.Value += signal_dash()
            elif letter == ' ':
                for x in range(int(max(self.Bit_rate, self.Frequency + 100) * LENGTH_DOT)):
                    self.Value += chr(0)

    # CONVERT CHAR SIGNAL TO SOUND VIA PyAudio
    def generate_buffer_sound(self):

        # Create an in-memory bytes buffer
        audio_data = bytes(self.Value, 'latin1')
        audio_buffer = BytesIO()
        # put the data in the buffer
        with wave.open(audio_buffer, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(1)  # 1 byte per sample (8-bit PCM)
            wf.setframerate(self.Bit_rate)
            wf.writeframes(audio_data)

            # Move to the beginning of the BytesIO buffer
            audio_buffer.seek(0)

        return audio_buffer

    # SHOW THE VALUE OF THE SIGNAL ON PLOT
    def show_sound(self):
        # Convert signalDATA to numerical values
        signal_values = [ord(char) for char in self.Value]

        # Plot the signal form
        fig = plt.figure(figsize=(12, 4))
        plt.plot(signal_values, color='blue')
        plt.title("signalform Visualization of signalDATA")
        plt.xlabel("Sample Index")
        plt.ylabel("Amplitude (0 to 255)")
        plt.margins(x=0, y=0)

        # convert a figure to an html string using mpld3
        image = mpld3.fig_to_html(fig)
        pyperclip.copy(image)
        return image


# CREATE A SIGNAL
def generate_signal(freq, bit_rate, sample_length, fill=False):
    signal = ''
    bit_rate = max(bit_rate, freq + 100)
    nb_frames = int(bit_rate * sample_length)
    # Generate signal
    for x in range(nb_frames):
        signal += chr(int(math.sin(x / ((bit_rate / freq) / math.pi)) * 127 + 128))

    if fill:
        rest_frames = nb_frames % bit_rate
        for x in range(rest_frames):
            signal += chr(0)

    for x in range(int(bit_rate * LENGTH_DOT)):
        signal += chr(0)
    return signal


def signal_dot():
    return generate_signal(DEFAULT_FREQUENCY, DEFAULT_BIT_RATE, LENGTH_DOT)


def signal_dash():
    return generate_signal(DEFAULT_FREQUENCY, DEFAULT_BIT_RATE, LENGTH_DASH)


def generate_sound(buffer):
    with wave.open(buffer, 'rb') as wf:
        # Open PyAudio stream
        # Instantiate PyAudio and initialize PortAudio system resources (1)
        PyAudio = pyaudio.PyAudio
        p = PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read all data at once #Option could be to use chunk
        data = wf.readframes(wf.getnframes())
        # Play the audio by writing all data to the stream
        stream.write(data)

        # Stop the PyAudio stream
        stream.stop_stream()
        stream.close()
        p.terminate()
