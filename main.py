import logging
import os, sys

import webbrowser
import wikipedia
import pywhatkit
import pyautogui as pa
import threading
from time import sleep, strftime
import inspect
from functools import partial

from engine.engine import Engine
from features.default_features import default_apps
from features.comm_features import com_feat
from query_list.qry_list import qr

# from feature.process_monitor import browser_tabs_info_alter2
# from memory.q_list import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

list_data = qr.read_file()
nl = '\n'

# log_dir = '.\\log\\'
log_dir = './log'
# file_name = time.strftime("%Y-%m-%d") + '_Vaani.log'
file_name = strftime("%Y-%m-%d") + '_Vaani.log'
# full_file_path = log_dir + '/' + file_name
filepath = log_dir + '/' + file_name
# os.chdir(log_dir)
print(f'full_file_path:\t{filepath}')

# logging.basicConfig(filepath,
#                     filemode='w',
#                     format='%(name)s - %(levelname)s - %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG,
#                     force=True)

logging.info('Logger Initiated >>> ')
logger = logging.getLogger('Logger Initiated >>> ')


# log_file = config_parsar.read_config()
# print('Log File:\t', log_file)

class VaaniVA:
    def __init__(self, filepath):
        self.filepath = filepath
        # self.filepath = filepath

    def get_logger(self):
        logging.basicConfig(filename=filepath, filemode='w',
                            level=logging.DEBUG,
                            format='%(name)s - %(levelname)s - %(message)s')
        logging.debug(">> Logging initiated :: ")
        return logging.getLogger(__name__)

    # logger = get_logger('./log/log.txt')
    # logger.info('> Logger initiate!')

    def Hello(self):
        logger.info('>> Initiate greet message. ')
        # Engine.Speak(
        return Engine.Speak('Hello sir I am Vaani, your virtual assistant. Tell me how may I help you')

    def non_service_task(self):
        Engine.Speak('Service Not added yet')
        pass

    # def query_action(self, qry: str, srch_str: list, action, action_filter: str):
    #     for i in range(len(srch_str)):
    #         srch_str = srch_str[i]
    #         # test_mod_new = WebSearch(srch_str)
    #         # print(f'Test report:\t{test_mod_new}')
    #         print(f'Search str:\t{srch_str}')
    #         try:
    #             if srch_str in qry:
    #                 if not hasattr(action, action_filter):
    #                     if action == callable:
    #                         print(f'Param is a function')
    #                         action_filter = None
    #                         action = partial(action, action_filter)
    #                         Engine.Speak(f'Function:{action}')
    #                         pass
    #                     else:
    #                         self.non_service_task()
    #                 else:
    #                     action = partial(action, action_filter)
    #                 return action
    #         except 'IndexError':
    #             pass
    #         else:
    #             self.non_service_task()

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
            return self.get_action(com_feat.open_window(), None)
        elif list_name == 'StopKeywords_cmd_list':
            return self.get_action(default_apps.end_assistant(), None)
        else:
            pass

    def get_action(self, action, action_filter):
        if action_filter is not None:
            print(f'Param is a function with Action_filter values')
            action = partial(action, action_filter)
            return action
        else:
            if action == callable:
                print(f'Param is a function')
                # action_filter = None
                action = partial(action, None)
                Engine.Speak(f'Function:{action}')
                pass
            return action

    def query_action1(self, qry: str, srch_str: str, action, action_filter: str):
        try:
            if srch_str in qry:
                if not hasattr(action, action_filter):
                    if action == callable:
                        print(f'Param is a function')
                        action_filter = None
                        action = partial(action, action_filter)
                        Engine.Speak(f'Function:{action}')
                        pass
                    else:
                        self.non_service_task()
                else:
                    action = partial(action, action_filter)
                return action
            else:
                self.non_service_task()
        except 'IndexError':
            pass

    def dict_ops(self, dict_str: dict):
        trans_val = ''
        print(f'InPut Dict:\t{dict_str}')
        # print(f'Dict_keys:\t{dict_str.keys()}')
        # print(f'Alternative_items:\t{dict_str["alternative"]}')
        try:
            if dict_str is not None:
                if type(dict_str) == dict:
                    alter_val = dict_str["alternative"]
                    for p in range(len(alter_val)):
                        trans_val = alter_val[p]["transcript"]
                        print(f'Trans_val:\t{trans_val}')
                        return trans_val
                elif type(dict_str) == list:
                    pass
                else:
                    pass
            else:
                pass
        except:
            pass

    def TakeQuery(self):
        """
        :return: action none
        """
        logger.info(">> Initiating query input.  ")
        wake_word = "are you up there"
        self.Hello()
        logger.info(">> Welcome message to begin interaction. ")
        while True:
            logger.info(">> Convert Speech to text into Lower case. ")
            query = Engine.take_command()  # .lower()
            query = self.dict_ops(query)
            print(f'Type of Query:\t{type(query)}')
            print(f'Query Without Loop:\t{query}')
            logger.info(">> Pre-set checks for matching pre defined commands. ")
            k = qr.key_by_val(list_data, query)
            print(f'List name in Main:\t{k}{nl}Finalize Query before trigger Command:\t{query}')
            self.cmd_relay(k, query)
            # return action_cmd


if __name__ == '__main__':
    # logger.info('> Initiated speech reorganization system. ')
    VA = VaaniVA(filepath)
    VA.TakeQuery()

