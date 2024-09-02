import signal
import morse
from flask import Flask, render_template, send_file, Response, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import mpld3

SECRET_KEY = "KEY"

# -----------------MAIN------------------------
WAVEDATA = signal.Signal() # Global WAVEDATA to store sound

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
        global WAVEDATA
        converted_text = morse.word_to_morse(form.Text.data)
        WAVEDATA.morse_to_signal(converted_text)
        return render_template('home.html', form=form, result=converted_text, WAVEDATA=WAVEDATA)
    return render_template('home.html', form=form)

@app.route('/generate_audio', methods=['GET', 'POST'])
def generate_audio():
    global WAVEDATA
    sound = WAVEDATA.generate_buffer_sound()
    return Response(sound)

if __name__ == "__main__":
    app.run()

