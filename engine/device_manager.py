import pyaudio
import speech_recognition as sr
import logging
from engine.engine import Engine


class DeviceManager:
    def __init__(self):
        self.pyaudio_instance = pyaudio.PyAudio()
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.speaker = None

    def list_devices(self):
        device_count = self.pyaudio_instance.get_device_count()
        devices = []
        for i in range(device_count):
            device_info = self.pyaudio_instance.get_device_info_by_index(i)
            devices.append(device_info)
        return devices

    def set_input_device(self, device_index):
        self.microphone = sr.Microphone(device_index=device_index)

    def set_output_device(self, device_index):
        self.speaker = device_index
        self.pyaudio_instance.terminate()
        self.pyaudio_instance = pyaudio.PyAudio()

    def get_input_devices(self):
        return [device for device in self.list_devices() if device['maxInputChannels'] > 0]

    def get_output_devices(self):
        return [device for device in self.list_devices() if device['maxOutputChannels'] > 0]

    def listen(self):
        with self.microphone as source:
            logging.debug("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)
            logging.debug("Listening for speech...")
            audio = self.recognizer.listen(source)
            return audio

    def recognize_speech(self, audio):
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            logging.debug("Could not understand audio")
        except sr.RequestError as e:
            logging.debug(f"Could not request results; {e}")

    def handle_errors(self):
        logging.debug("Listening timed out. Restarting listening process.")
        devices = self.get_input_devices()
        if not devices:
            logging.debug("No input devices available.")
            return False

        self.set_input_device(devices[0]['index'])
        return True


