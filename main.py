import pandas as pd

df = pd.read_csv('morse.csv', names=['CHAR', 'MORSE'], header=None)
to_convert = input('Enter a word : ').upper()
converted = ""

for letter in to_convert:
    converted += df.MORSE[df.CHAR == letter].values[0]
    converted += " "

print(converted)
