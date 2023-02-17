import speech_recognition as sr

mics =sr.Microphone.list_microphone_names()

for mic in mics:
    print(mic)

