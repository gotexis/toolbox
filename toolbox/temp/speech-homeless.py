import speech_recognition as sr
from os import path


AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), 'dave-AS6MAxN4-20190131.mp3.wav')


r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file

try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
