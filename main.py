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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

list_data = qr.read_file()
nl = '\n'

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_dir = './logs/'
file_name = strftime("%Y-%m-%d") + '_Vaani.logs'
filepath = log_dir + '/' + file_name
# os.chdir(log_dir)
print(f'full_file_path:\t{filepath}')


class VaaniVA:
    def __init__(self):
        # self.filepath = filepath
        # self.filepath = filepath
        self.get_logger()

    def get_logger(self):
        logging.basicConfig(filename=filepath, filemode='w',
                            level=logging.DEBUG,
                            format='%(name)s - %(levelname)s - %(message)s',
                            force=True)
        logging.debug(">> Logging initiated :: ")
        # return logging.getLogger(__name__)

    def Hello(self):
        # Engine.Speak(
        return Engine.Speak('Hello sir I am Vaani, your virtual assistant. Tell me how may I help you')

    def non_service_task(self):
        Engine.Speak('Service Not added yet')
        pass

    # TODO: Mute & Silent feature with simulteniously manage different works.
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
        elif list_name == 'SystemOff_cmd_list':
            return self.get_action(default_apps.system_down(), None)
        elif list_name == 'SystemLock_cmd_list':
            return self.get_action(default_apps.sys_lock(), None)
        elif list_name == 'RecycleBin_Cln_cmd_list':
            return self.get_action(default_apps.cln_trsh(), None)
        elif list_name == 'ConsoleCln_list_cmd':
            return self.get_action(default_apps.cmd_clr(), None)
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
        wake_word = "are you up there"
        query = Engine.take_command()  # .lower()
        if query is not None:
            query = self.dict_ops(query)
            print(f'Type of Query:\t{type(query)}')
            print(f'Query Without Loop:\t{query}')
            return query
        elif query == []:
            Engine.Speak(f'can you repeat that once again! its an empty list')
            pass
        else:
            Engine.Speak(f'can you repeat that once again!')
            pass


if __name__ == '__main__':
    VA = VaaniVA()
    # VA.get_logger()
    VA.Hello()
    #TODO: Multi Process add & manage process.
    while True:
        query = VA.TakeQuery()
        k = qr.key_by_val(list_data, query)
        print(f'List name in Main:\t{k}{nl}Finalize Query before trigger Command:\t{query}')
        VA.cmd_relay(k, query)


