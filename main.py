import wave
import morse
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

SECRET_KEY = "KEY"

# ----------------- RETRIEVE WORD FROM USER -----------------
to_convert = "GRACE"  # input('Enter a word : ').upper()
converted = morse.word_to_morse(to_convert)
print(converted)

# -----------------MAIN------------------------
# WAVEDATA = wave.Wave()
# WAVEDATA.morse_to_wave(converted)
# WAVEDATA.generate_sound()
# WAVEDATA.show_sound()

# -----------------WEB APP -------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
boostrap = Bootstrap5(app)

# FORM
class Myform(FlaskForm):
    Text = StringField('Text to convert :', validators=[DataRequired()])
    Submit = SubmitField('Convert')

@app.route("/", methods=['GET', 'POST'])
def home():
    form = Myform()
    if form.validate_on_submit():
        converted_text = morse.word_to_morse(form.Text.data)
        WAVEDATA = wave.Wave()
        WAVEDATA.morse_to_wave(converted)
        WAVEDATA.show_sound()
        return render_template('home.html', form=form, result=converted_text)
    return render_template('home.html', form=form)

if __name__ == "__main__":
    app.run()

