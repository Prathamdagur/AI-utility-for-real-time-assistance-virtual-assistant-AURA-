import speech_recognition as sr
import pyttsx3
from model import CommandProcessor
import time

# Create ONE engine globally!
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print(f"Assistant says: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.15)  # Prevents buffer bug

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    processor = CommandProcessor()

    print("Calibrating microphone (please be quiet)...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Calibration done.")

    speak("Hello! I'm your voice assistant. How can I help you?")

    while True:
        try:
            with microphone as source:
                print("\nListening...")
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)
            try:
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                response = processor.process(command)
                print(f"Response: {response}")
                speak(response)
                if "exit" in command.lower() or "goodbye" in command.lower():
                    break
            except sr.UnknownValueError:
                print("Speech not understood")
                speak("I didn't catch that. Could you repeat?")
            except sr.RequestError:
                print("Speech recognition API error")
                speak("Sorry, there was an error with the speech recognition service.")
        except Exception as e:
            print(f"Listening error: {str(e)}")
            speak("Sorry, I had trouble listening.")

    speak("Goodbye! Have a great day.")

if __name__ == "__main__":
    main()
