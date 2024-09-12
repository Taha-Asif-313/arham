import speech_recognition as sr
import time

recognizer = sr.Recognizer()

print(sr.Microphone.list_microphone_names())  # Print available microphones

# Choose the microphone index or name based on your system configuration
microphone_index = 0  # Adjust this index based on your system

with sr.Microphone(device_index=microphone_index) as source:
    recognizer.adjust_for_ambient_noise(source)

    while True:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        time.sleep(1)  # Adjust sleep time as needed
