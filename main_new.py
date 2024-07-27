import logging
import os
import sys
import time
from functools import partial
import concurrent.futures
import webrtcvad
from pydub import AudioSegment
from pydub.utils import make_chunks
import threading


from engine.engine_updated import Engine
from features.comm_features import com_feat
from features.default_features import default_apps
from query_list.qry_list import qr
from engine.device_manager import DeviceManager
from engine.query_compiler import CQ
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

list_data = qr.read_file()
nl = '\n'

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_dir = './logs/'
file_name = time.strftime("%Y-%m-%d") + '_Vaani.logs'
filepath = os.path.join(log_dir, file_name)
print(f'full_file_path:\t{filepath}')


def fetch_config():
    response = requests.get('http://127.0.0.1:5000/api/config')
    return response.json()


class VaaniVA:
    def __init__(self):
        self.config = fetch_config()  # Fetch configuration from Flask app
        print(f'get Config from app server\t::{self.config}')
        self.get_logger()
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(1)  # 0-3. 3 is the most aggressive about filtering out non-speech

    def get_logger(self):
        logging.basicConfig(filename=filepath, filemode='w',
                            level=logging.DEBUG,
                            format='%(name)s - %(levelname)s - %(message)s',
                            force=True)
        logging.debug(">> Logging initiated :: ")

    def Hello(self):
        return Engine.Speak('Hello sir I am Vaani, your virtual assistant. Tell me how may I help you')

    def non_service_task(self):
        Engine.Speak('Service Not added yet')
        pass

    def is_speech(self, audio_chunk):
        """ Check if the audio chunk contains speech. """
        return self.vad.is_speech(audio_chunk, 16000)

    def filter_non_speech(self, audio):
        """ Filter out non-speech parts from the audio. """
        audio_chunks = make_chunks(audio, 30)  # split audio into 30ms chunks
        speech_audio = AudioSegment.empty()
        for chunk in audio_chunks:
            if self.is_speech(chunk.raw_data):
                speech_audio += chunk
        return speech_audio

    def cmd_relay(self, list_name, inp_str):
        print(f'Getting input String\t:{inp_str}{nl} Getting List Name\t:{list_name}')
        if list_name == 'WebSearch_cmd_list':
            return self.get_action(com_feat.google_search(inp_str), None)
        elif list_name == 'WakeKeywords_cmd_list':
            return self.get_action(com_feat.wake_up_cmd(), None)
        elif list_name == 'WikiSearch_cmd_list':
            return self.get_action(com_feat.wikipedia_search(inp_str), None)
        elif list_name == 'TimeReminder_cmd_list':
            return self.get_action(com_feat.tell_time(), None)
        elif list_name == 'DayReminder_cmd_list':
            return self.get_action(com_feat.get_today(), None)
        elif list_name == 'Intro_cmd_list':
            return self.get_action(com_feat.name_intro(), None)
        elif list_name == 'YtMusic_cmd_list':
            return self.get_action(com_feat.play_music(inp_str), None)
        elif list_name == 'NoteCreate_cmd_list':
            return self.get_action(com_feat.make_note(), None)
        elif list_name == 'ApplicationWindowOpen_cmd_list':
            # Updated to handle window switching
            return self.get_action(lambda: com_feat.open_window(inp_str), None)
        elif list_name == 'StopKeywords_cmd_list':
            return self.get_action(default_apps.end_assistant(), None)
        elif list_name == 'SystemOff_cmd_list':
            return self.get_action(default_apps.system_down(), None)
        elif list_name == 'SystemLock_cmd_list':
            return self.get_action(default_apps.sys_lock(), None)
        elif list_name == 'RecycleBin_Cln_cmd_list':
            return self.get_action(default_apps.cln_trsh(), None)
        elif list_name == 'ConsoleCln_list_cmd':
            return self.get_action(default_apps.cmd_clr(), None)
        elif list_name == 'Mute_sound':
            return self.get_action(default_apps.mute_system_sound(), None)
        elif list_name == 'Unmute_sound':
            return self.get_action(default_apps.unmute_system_sound(), None)
        else:
            return Engine.Speak('Please repeat your query again')

    def get_action(self, action, action_filter):
        if action_filter is not None:
            print(f'Param is a function with Action_filter values')
            action = partial(action, action_filter)
            return action
        else:
            if action == callable:
                print(f'Param is a function')
                action = partial(action, None)
                Engine.Speak(f'Function:{action}')
                pass
            return action

    def dict_ops(self, dict_str: dict):
        trans_val = ''
        print(f'InPut Dict:\t{dict_str}')
        try:
            if dict_str is not None:
                if type(dict_str) == dict:
                    alter_val = dict_str["alternative"]
                    for p in range(len(alter_val)):
                        trans_val = alter_val[p]["transcript"]
                        print(f'Trans_val:\t{trans_val}{nl}typ:\t{type(trans_val)}')
                        return trans_val
                elif type(dict_str) == list:
                    pass
                else:
                    pass
            else:
                pass
        except Exception as e:
            print(f"Error processing dictionary: {e}")

    def TakeQuery(self):
        query = Engine.take_command()  # .lower()
        if query is not None:
            query = self.dict_ops(query)
            return query
        elif not query:
            Engine.Speak(f'can you repeat that once again!')
            return []
        else:
            Engine.Speak(f'can you repeat that once again!')
            return []

    def listen_and_act(self):
        while True:
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor_for_query:
                    get_query = executor_for_query.submit(self.TakeQuery)
                    returned_query = get_query.result(timeout=10)  # Timeout after 10 seconds

                if returned_query:
                    get_key_element = qr.key_by_val(list_data, returned_query)
                    returned_action = self.cmd_relay(get_key_element, returned_query)
                    if callable(returned_action):
                        # Start a new thread for the action
                        action_thread = threading.Thread(target=self.execute_action, args=(returned_action,))
                        action_thread.start()
            except concurrent.futures.TimeoutError:
                print("Listening timed out. Restarting listening process.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def execute_action(self, action):
        try:
            action()  # Execute the action if it's callable
        except Exception as e:
            print(f"Error executing action: {e}")


if __name__ == '__main__':
    start_time_counter = time.time()
    active_word = "I'm up here"
    VA = VaaniVA()
    VA.Hello()

    dm = DeviceManager()
    input_devices = dm.get_input_devices()
    output_devices = dm.get_output_devices()

    if input_devices:
        dm.set_input_device(input_devices[0]['index'])
    else:
        logging.debug("No input devices found.")

    if output_devices:
        dm.set_output_device(output_devices[0]['index'])
    else:
        logging.debug("No output devices found.")

    while True:
        try:
            audio = dm.listen()
            returned_query = dm.recognize_speech(audio)
            print(f'User query\t{returned_query}')

            get_key_element = qr.key_by_val(list_data, returned_query)
            returned_action = VA.cmd_relay(get_key_element, returned_query)
        except Exception as e:
            logging.debug(f"Error: {e}")
            if not dm.handle_errors():
                break
