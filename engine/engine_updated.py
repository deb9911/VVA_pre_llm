import threading
import queue
import speech_recognition as sr
import pyttsx3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from context_manager import ContextManager
import requests
from pywhatkit.core.exceptions import InternetException

nltk.data.path.append('./nltk_data')


class Engine:
    recognizer = sr.Recognizer()
    context_manager = ContextManager()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    tts_engine = pyttsx3.init()

    def __init__(self):
        self.tts_queue = queue.Queue()
        self.tts_thread = threading.Thread(target=self.run_tts)
        self.tts_thread.daemon = True
        self.tts_thread.start()

    def run_tts(self):
        while True:
            text = self.tts_queue.get()
            if text is None:
                break
            voices = self.tts_engine.getProperty('voices')
            self.tts_engine.setProperty('voice', voices[1].id)
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.tts_queue.task_done()

    def take_command(self):
        with sr.Microphone() as source:
            Engine.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = Engine.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            try:
                command = Engine.recognizer.recognize_google(audio, language='en-US')
                print(f"Recognized command: {command}")
                processed_command = self.process_command(command)
                self.context_manager.set("last_command", processed_command)
                return processed_command
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return None
            except sr.RequestError:
                print("Sorry, there was an issue with the speech recognition service.")
                return None

    def process_command(self, command):
        tokens = word_tokenize(command)
        filtered_tokens = [word for word in tokens if word.lower() not in self.stop_words]
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in filtered_tokens]
        tagged_tokens = pos_tag(lemmatized_tokens)
        print(f"Processed command: {tagged_tokens}")
        return tagged_tokens

    def Speak(self, text):
        print(f"Queueing text for speech: {text}")
        self.tts_queue.put(text)
        self.context_manager.set("last_spoken_text", text)

    @staticmethod
    def check_internet_connection():
        try:
            requests.get('https://www.google.com', timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def run_feature(self):
        if self.check_internet_connection():
            try:
                # Example usage of a pywhatkit function that requires the internet
                # Replace this with your actual pywhatkit feature
                # kit.sendwhatmsg("+1234567890", "Hello", 15, 0)  # Just an example function
                print("Running internet-dependent feature.")
            except InternetException:
                print("No internet connection. Please check your connection and try again.")
                self.Speak("It seems I am unable to connect to the internet. Please check your connection.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                self.Speak("An unexpected error occurred. Please try again.")
        else:
            print("Offline mode: Some features are unavailable.")
            self.Speak("You are currently offline. Some features may not be available.")

    def shutdown(self):
        self.tts_queue.put(None)
        self.tts_thread.join()


engine = Engine()
# Example usage
# if __name__ == "__main__":
#     engine = Engine()
#     command = engine.take_command()
#     if command:
#         engine.Speak("You said: " + ' '.join([word for word, tag in command]))
#     engine.run_feature()  # Call to run feature that may need internet
#     engine.shutdown()
