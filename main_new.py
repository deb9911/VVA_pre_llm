import logging
import os
import sys
import time
from functools import partial
from time import strftime
import concurrent.futures

from engine.engine import Engine
from features.comm_features import com_feat
from features.default_features import default_apps
from query_list.qry_list import qr
from engine.query_compiler import CQ
# from models.llm_config import llama2, llama2_response_store


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

list_data = qr.read_file()
nl = '\n'

log_dir = './logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
file_name = strftime("%Y-%m-%d") + '_Vaani.logs'
filepath = os.path.join(log_dir, file_name)

# Configuring the logger
logging.basicConfig(filename=filepath, filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
print(f'Logging started. Log file at: {filepath}')
logger.info(f'Logging started. Log file at: {filepath}')


class VaaniVA:
    def __init__(self):
        self.engine = Engine()

    def Hello(self):
        logger.info('Greeting user.')
        return self.engine.Speak('Hello sir I am Vaani, your virtual assistant. Tell me how may I help you')

    def non_service_task(self):
        logger.warning('Non-service task invoked.')
        self.engine.Speak('Service Not added yet')
        pass

    def cmd_relay(self, list_name, inp_str):
        logger.info(f'cmd_relay invoked with list_name: {list_name} and inp_str: {inp_str}')
        try:
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
                return self.get_action(com_feat.open_window(), None)
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
                logger.warning('Command not recognized.')
                return self.engine.Speak('Please repeat your query again')
        except Exception as e:
            logger.error(f'Error in cmd_relay: {e}')

    def get_action(self, action, action_filter):
        if callable(action):
            logger.info('Executing action.')
            action = partial(action, action_filter)
            return action
        else:
            logger.warning('Action is not callable.')
            return None

    def dict_ops(self, dict_str: dict):
        trans_val = ''
        logger.debug(f'dict_ops invoked with dict_str: {dict_str}')
        try:
            if dict_str is not None:
                if isinstance(dict_str, dict):
                    alter_val = dict_str["alternative"]
                    for p in range(len(alter_val)):
                        trans_val = alter_val[p]["transcript"]
                        logger.info(f'Trans_val: {trans_val}')
                        return trans_val
                elif isinstance(dict_str, list):
                    pass
                else:
                    pass
            else:
                pass
        except Exception as e:
            logger.error(f'Error in dict_ops: {e}')

    def TakeQuery(self):
        """
        :return: action none
        """
        logger.info('Listening for query...')
        query = self.engine.take_command()
        if query is not None:
            query = self.dict_ops(query)
            logger.info('Dict Ops executed')
            return query
        elif query == []:
            logger.info('query is an empty list')
            self.engine.Speak(f'can you repeat that once again!')
            return None
        else:
            logger.info('Dict Ops executed')
            self.engine.Speak(f'Did not get you. ')
            return None
            pass


if __name__ == '__main__':
    start_time_counter = time.time()
    active_word = "I'm up here"
    VA = VaaniVA()
    VA.Hello()
    max_attempts = 10  # Maximum number of attempts to listen for a query
    attempt_count = 0

    while attempt_count < max_attempts:
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor_for_query:
                get_query = executor_for_query.submit(VA.TakeQuery)
                returned_query = get_query.result()

            if returned_query:
                get_key_element = qr.key_by_val(list_data, returned_query)
                returned_action = VA.cmd_relay(get_key_element, returned_query)
                if callable(returned_action):
                    if returned_action:
                        attempt_count = 0  # Reset attempt counter if a valid action is found
            else:
                attempt_count += 1

            time.sleep(0.5)  # Adding a small delay to avoid tight loop
        except Exception as e:
            logger.error(f"An error occurred: {e}")
