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
                            level=logging.INFO,
                            format='%(name)s - %(levelname)s - %(message)s',
                            force=True)
        logging.debug(">> Logging initiated :: ")
        # var = logging.INFO
        return logging.getLogger(__name__)
        # return var

    def Hello(self):
        # Engine.Speak(
        return Engine.Speak('Hello sir I am Vaani, your virtual assistant. Tell me how may I help you')

    def non_service_task(self):
        Engine.Speak('Service Not added yet')
        pass

    # TODO: Mute & Silent feature with simultaneously manage different works.
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
        elif list_name == 'Mute_sound':
            return self.get_action(default_apps.mute_system_sound(), None)
        elif list_name == 'Unmute_sound':
            return self.get_action(default_apps.unmute_system_sound(), None)
        # elif list_name == "LLM_Response":
        #     llm_response = llama2(inp_str)
        #     response_str = llama2_response_store(llm_response)
            # return self.get_action(llama2(inp_str), None)
            # print(f'llm_response:\t{llm_response}{nl}Type:\t{type(llm_response)}')  # TODO: Response is very slow. Fixme
            # llm_response = str(llm_response)
            # print(f'llm_response\t:~~~~~~~::{llm_response}{nl}'
            #       f'{nl}LLM_Response_type:\t::{type(llm_response)}')
            # return Engine.Speak(response_str)
        else:
            # return Engine.Speak('Can you repeat your query')
            return Engine.Speak('Please repeat your query again')

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
                        print(f'Trans_val:\t{trans_val}{nl}typ:\t{type(trans_val)}')
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
        query = Engine.take_command()  # .lower()
        if query is not None:
            query = self.dict_ops(query)
            # query = CQ.query_fixer(query)
            return query
        elif query == []:
            Engine.Speak(f'can you repeat that once again!')
            pass
        else:
            Engine.Speak(f'can you repeat that once again!')
            pass


if __name__ == '__main__':
    start_time_counter = time.time()
    active_word = "I'm up here"
    VA = VaaniVA()
    # VA.get_logger()
    VA.Hello()
    # TODO: Multi Process add & manage process.
    while 1:
        with concurrent.futures.ThreadPoolExecutor() as executor_for_query:
            get_query = executor_for_query.submit(VA.TakeQuery, )
            returned_query = get_query.result()

        get_key_element = qr.key_by_val(list_data, returned_query)
        returned_action = VA.cmd_relay(get_key_element, returned_query)


