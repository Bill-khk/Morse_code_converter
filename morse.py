import pandas as pd


class Morse:

    def __init__(self):
        pass


def word_to_morse(word):
    df = pd.read_csv('morse.csv', names=['CHAR', 'MORSE'], header=None)
    converted = ""

    for letter in word.upper():
        converted += df.MORSE[df.CHAR == letter].values[0]
        converted += " "
    return converted
