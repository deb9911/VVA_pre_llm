from tqdm import tqdm


def bar(process_name: str):
    if type(process_name) == str:
        desc = process_name
    else:
        desc = '>>\\ Process Name not defined'
    for i in tqdm(range(101),
                  desc=desc,
                  ascii=False, ncols=75):
        # time.sleep()
        pass
    print(f'Completed>> ')

## This is a simple progress bar, with the help of this progress bar,
# we can understad about high level analisys

