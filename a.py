import speech_recognition as sr
import time


recognizer = sr.Recognizer()
    # List available audio devices
print(sr.Microphone.list_microphone_names())