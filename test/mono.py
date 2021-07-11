import speech_recognition as sr
from scipy.io import wavfile
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

filepath = 'stereohappy.wav'
samplerate, data = wavfile.read(filepath)
r = sr.Recognizer()

out = []
if len(data.shape) != 1:
    data = data[:, 0]
write('monohappy.wav', samplerate, data)
