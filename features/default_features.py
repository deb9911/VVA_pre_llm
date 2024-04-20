import ctypes
import subprocess

import pdfplumber
import os
import datetime

import winshell as winshell

from engine.engine import Engine
import logging

file_type = {"txt": "text", "xlsx": "spreadsheet", "csv": "spreadsheet",
             "docs": "document", "pdf": 'pdf', "ini": "information",
             "py": "script", "js": "script", "cpp": "script"}

'''Open Files using specific apps through this class'''


class DefaultApps:
    qry = ''

    def file_recognizer(self):
        logging.debug(f'Initiate File recognizer. ')
        file_recogniser = file_type.keys()
        # if file_recogniser == 'txt':

    def tell_time(self):
        logging.debug(f'Initiate Time operation. ')
        # This method will give the time
        time = str(datetime.datetime.now())

        # the time will be displayed like
        # this "2020-06-05 17:50:14.582630"
        # nd then after slicing we can get time
        print(time)
        hour = time[11:13]
        mins = time[14:16]
        return hour, mins

    def tell_day(self):
        logging.debug(f'Initiate Day Operation. ')
        # This function is for telling the
        # day of the week
        day = datetime.datetime.today().weekday() + 1

        # this line tells us about the number
        # that will help us in telling the day
        day_dict = {1: 'Monday', 2: 'Tuesday',
                    3: 'Wednesday', 4: 'Thursday',
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}

        if day in day_dict.keys():
            day_of_the_week = day_dict[day]
            return day_of_the_week

    def check_file(filename, path):
        logging.debug(f'Initiate Check file process. ')
        filepath = str()
        dirs = {'home': os.path.expanduser,
                'downloads': os.path.expanduser('/Downloads'),
                'documents': os.path.expanduser('/Documents')
                }
        if path in dirs.keys():
            src_dir = os.path.dirname(os.path.abspath(filepath))
            # src_dir = os.chdir(src_dir)
            print('src_dir:\t', src_dir)
            filepath = src_dir + '\\' + filename
            print('File found:\t', filepath)
            return filepath

    def read_content(filepath):
        logging.debug(f'Initiate Reading content operation. ')
        pdf_text = ''
        with pdfplumber.open(filepath) as pdf:
            pages = pdf.pages
            for page in pages:
                pdf_text = page.extract_text()
            return pdf_text

    @staticmethod
    def google_search(qry: str):
        logging.debug(f'Initiate Google Search operation. ')
        """
        :param qry: str
        :return: str
        """
        if qry != '':
            try:
                from googlesearch import search
            except:
                print("No Module named <<Google Search>> ")

            for i in search(qry, tld="co.in", num=10, stop=10, pause=2):
                print("search value:\t", i)
                return i
        else:
            print(f'Empty String:\t{qry}')

    def cmd_clr(self):
        logging.debug(f'Initiate Clear console screen. ')
        clear = lambda: os.system('cls')
        return clear

    def sys_lock(self):
        logging.debug(f'Initiate System locking operation. ')
        ctypes.windll.user32.LockWorkStation()

    def system_down(self):
        logging.debug(f'Initiate Shut Down process. ')
        subprocess.call('shutdown / p /f')

    def cln_trsh(self):
        logging.debug(f'Initiate Clearn trash operation. ')
        return winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)

    def hibrnet(self):
        logging.debug(f'Initiate hibernet operation. ')
        return subprocess.call("shutdown / h")

    def sign_off(self):
        logging.debug(f'Initiate Signing off process. ')
        return subprocess.call(["shutdown", "/l"])

    def end_assistant(self):
        logging.debug(f'Initiate End of main process initiated. ')
        Engine.Speak("Bye")
        exit()


default_apps = DefaultApps()

