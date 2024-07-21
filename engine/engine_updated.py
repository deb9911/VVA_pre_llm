import threading
import speech_recognition as sr
import pyttsx3


class Engine:
    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()

    @staticmethod
    def take_command():
        with sr.Microphone() as source:
            print("Listening...")
            audio = Engine.recognizer.listen(source)
            try:
                command = Engine.recognizer.recognize_google(audio)
                print(f"Recognized command: {command}")
                return command
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                print("Sorry, there was an issue with the speech recognition service.")
                return None

    @staticmethod
    def Speak(text):
        print(f"Speaking: {text}")
        voices = Engine.tts_engine.getProperty('voices')
        # logger.info("Setting Speak engine property to Voices[1].id")
        Engine.tts_engine.setProperty('voice', voices[1].id)
        Engine.tts_engine.say(text)
        Engine.tts_engine.runAndWait()
