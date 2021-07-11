import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

import speech_recognition as sr
from scipy.io import wavfile
from scipy.io.wavfile import write
import numpy as np
import numpy.ma as ma

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

text = []
def split_phrases(filepath):
    samplerate, data = wavfile.read(filepath)

    if len(data.shape) == 1:
        data = np.array([data, data]).transpose()
    print(data)
    length = data.shape[0] / samplerate
    time = np.linspace(0., length, data.shape[0])

    mxamp = np.max(np.abs(data))

    filamp = np.where(np.abs(data) < mxamp * 0.01, 0, 1)

    ind = np.where(filamp == 1)[0]
    for i in range(1, len(ind)):
        if ind[i] - ind[i - 1] < samplerate * 0.1:
            for j in range(ind[i - 1], ind[i]):
                filamp[j][:] = 1
    ind = np.where(filamp == 0)[0]

    for i in range(1, len(ind)):
        if ind[i] - ind[i - 1] < samplerate * 0.1:
            for j in range(ind[i - 1], ind[i]):
                filamp[j][:] = 0
    filamp[0][:] = 0
    filamp[-1][:] = 0
    ind = np.where(filamp == 0)[0]

    ct = 0
    r = sr.Recognizer()
    out = []
    for i in range(1, len(ind)):
        if ind[i] - ind[i - 1] > 1:
            write(f'out/out{ct}.wav', samplerate, data[ind[i - 1] : ind[i]])
            with sr.AudioFile(f'out/out{ct}.wav') as source:
                audio_data = r.record(source)
                try:
                    text = r.recognize_google(audio_data)
                    print(text)
                    out.append(text)
                except sr.UnknownValueError:
                    print('?')
            ct+=1
    return out

@app.route('/analysis', methods=["GET"])
def analysis():
    return render_template('analysis.html')

@app.route('/evaluate', methods=['GET'])
def evaluate():
    print(text)
    return render_template('evaluate.html', text = text)

@app.route('/', methods=['GET', 'POST'])
def home():
    global text
    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('file saved')
        text = split_phrases(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(text)
        return redirect('/evaluate')
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)