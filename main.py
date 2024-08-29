import wave
import morse

# ----------------- RETRIEVE WORD FROM USER -----------------
to_convert = "AUDIO"  # input('Enter a word : ').upper()
converted = morse.word_to_morse(to_convert)
print(converted)

# -----------------MAIN------------------------
WAVEDATA = wave.Wave()
WAVEDATA.morse_to_wave(converted)
WAVEDATA.generate_sound()
WAVEDATA.show_sound()

