import pyttsx3
import speech_recognition as sr
import logging

import logging_config

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
# logger = logging.getLogger(__name__)
logger = logging_config.get_logger(__name__)


class Engine:
    r = sr.Recognizer()
    engine_model = pyttsx3.init()
    audio_str = ''
    query = dict

    @staticmethod
    def take_command():
        logger.info(f'Initiating Command taking function')
        with sr.Microphone() as source:
            logger.info(f'Initiate input device as Micro phone')
            audio = Engine.r.listen(source=source)
        try:
            print("Recognizing")
            logger.info(f'Source input processing. -- Voice input proces')
            query = Engine.r.recognize_google(audio, language='en-in', show_all=True)
            if type(query) == list:
                print(f'Query_type:\t{type(query)}')
                print(f'Query:\t{query}')
                # query = r.recognize_google(audio, language='en-in')
                # usr_query = r.recognize_sphinx (audio, language='en-US')
                print("the command is printed=", query)
                return query
            elif type(query) == dict:
                return query
            else:
                Engine.Speak("Repeat your query Please>> ")
                pass
        except 'speech_recognition.UnknownValueError':
            logger.info(f'speech_recognition.UnknownValueError')
            pass
        except Exception as e:
            logger.info(f'Exception happened at \t{e}')
            logger.exception("Audio input not recognized. ")
            print(e)
            print("Say that again")
            Engine.Speak("Say that again")
            logger.info("Return None. ")
            return "None"
        logger.info("Returning Query output, taken as audio input. ")

    @staticmethod
    def Speak(audio_str):
        if audio_str != '':
            voices = Engine.engine_model.getProperty('voices')
            logger.info("Setting Speak engine property to Voices[1].id")
            Engine.engine_model.setProperty('voice', voices[1].id)
            logger.info("Audio Output returned. ")
            Engine.engine_model.say(audio_str)
            logger.info("Initiated Run & Wait process for better complexity. ")
            Engine.engine_model.runAndWait()
        else:
            Engine.engine_model.say('The String is empty!!!')


engine = Engine()
