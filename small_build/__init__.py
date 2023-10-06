from functools import partial
from time import sleep, strftime

from engine.engine import Engine
from features.default_features import default_apps
from features.comm_features import com_feat
# from query_list.qry_list import qr, data


def get_action(action, action_filter):
    if action_filter is not None:
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

    # if not hasattr(action, action_filter):
    #     if action == callable:
    #         print(f'Param is a function')
    #         action_filter = None
    #         action = partial(action, action_filter)
    #         Engine.Speak(f'Function:{action}')
    #         pass
    #     else:
    #         pass
    # else:
    #     action = partial(action, action_filter)
    # return action


if __name__ == '__main__':
    inp_str = input('')
    get_action(com_feat.google_search(inp_str), None)

