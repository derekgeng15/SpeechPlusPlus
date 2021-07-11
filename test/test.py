import speech_recognition as sr
from scipy.io import wavfile
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

filepath = 'testaudio/pradapoop.wav'
samplerate, data = wavfile.read(filepath)
r = sr.Recognizer()

if len(data.shape) == 1:
    data = np.array([data, data]).transpose()
# print(data)
length = data.shape[0] / samplerate
time = np.linspace(0., length, data.shape[0])

mxamp = np.max(np.abs(data))

filamp = np.where(np.abs(data) < mxamp * 0.01, 0, 1)

ind = np.where(filamp == 1)[0]
# print(ind)
for i in range(1, len(ind)):
    if ind[i] - ind[i - 1] < samplerate * 0.1:
        for j in range(ind[i - 1], ind[i]):
            filamp[j][:] = 1
ind = np.where(filamp == 0)[0]

for i in range(1, len(ind)):
    if ind[i] - ind[i - 1] < samplerate * 0.1:
        for j in range(ind[i - 1], ind[i]):
            filamp[j][:] = 0
# print(ind)
# print(filamp)
filamp[0][:] = 0
filamp[-1][:] = 0
plt.figure(1)
plt.plot(time, filamp[:,0], label="left filter Channel")
# plt.plot(time, filamp[:,1], label="right filter Channel")
plt.figure(2)
plt.plot(time, data[:,0], label="left Channel")
# plt.plot(time, data[:,1], label="right Channel")
# plt.legend()

ind = np.where(filamp == 0)[0]
ct = 0
for i in range(1, len(ind)):
    if ind[i] - ind[i - 1] > 1:
        write(f'out/out{ct}.wav', samplerate, data[ind[i - 1] : ind[i]])
        with sr.AudioFile(f'out/out{ct}.wav') as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
                print(text)
            except sr.UnknownValueError:
                print('?')
        ct+=1
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

# write('new.wav', samplerate, data)