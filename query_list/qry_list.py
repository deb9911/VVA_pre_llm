import os
import json


src_file = r'query_list/cmd.json'
# src_file = r'query_list/cmd.json'
nl = '\n'


class CmdParser:
    def read_file(self):
        print(f'PWD:\t{os.getcwd()}')
        with open(src_file, 'r') as cmd:
        # with open(r'../query_list/cmd.json', 'r') as cmd:
            data = json.load(cmd)
            # print(f'Data: \t{data}')
            return data

    def key_list(self, data):
        print(f'Data>>>>>:\t{data.keys()}')
        key = list(data.keys())
        print(f'Key:\t{key}')
        for i in range(len(key)):
            key_name = key[i]
            print(f'Key_name:\t{type(key_name)}')
        return key

    def get_val(self, data, key_word):
        if len(key_word) != 0:
            if data[key_word]:
                val = data[key_word]
                print(f'Val:\t{val}')
                for i in range(len(val)):
                    qry_elmt = val[i]
                    print(f'Qry_elmnt:\t{qry_elmt}')
                    return val, qry_elmt
            else:
                print(f'Key Not matching')
        else:
            print(f'Empty string')

    def key_by_val(self, data, val_str: str):
        if val_str is not None:
            val_str = val_str.lower()
        else:
            pass
        match = False
        for k, v in data.items():
            if v is not None:
                for vm in range(len(v)):
                    act_val = v[vm]
                    # print(f'Actual_VAL:\t{act_val}{nl}Val_str:\t{val_str}')
                    if val_str is not None:
                        if act_val in val_str:
                            match = True
                            print(f'Key<<<>>>>>>:\t{k}')
                            return k
                        else:
                            match = False
                            pass
                    else:
                        pass
            else:
                print(f'Data not sorted')


qr = CmdParser()

# if __name__ == '__main__':
    # src_file = r'cmd.json'
    # qr = CmdParser()
# data = qr.read_file()
# key = qr.key_list(data)
# # val = qr.get_val(data, 'WebSearch_cmd_list')
# act_val, k = qr.key_by_val(data, 'in wikipedia')

