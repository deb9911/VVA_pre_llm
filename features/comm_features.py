import os
import sys
import webbrowser
import wikipedia
import pywhatkit
import pyautogui as pa
import datetime
from googlesearch import search
import logging

from engine.engine import Engine
from features import default_apps
from time import strftime, sleep


class CommonFeatures:

    # FIXME: replace_str can be routed from Command list script.
    @staticmethod
    def qry_filter(qry: str, replace_str: list):
        logging.debug(f'Initiate Query filter operation. ')
        if qry is not None:
            for r in range(len(replace_str)):
                print(f'Qry from Common Features:\t{qry}')
                qry = qry.replace(replace_str[r], "")
                return qry
        else:
            Engine.Speak("Empty Query>>> ")

    def open_google(self):
        logging.debug(f'Initiate Open google operartion. ')
        Engine.Speak("Opening Google ")
        return webbrowser.open("www.google.com")

    def google_search(self, query):
        logging.debug(f'Initiate Search content from google operation. ')
        Engine.Speak('Checking in Google')
        print(f'Unfiltered Query:\t{query}')
        query = self.qry_filter(query, ['search in google', 'find from google'])
        print(f'Filtered query:\t{query}')
        # result = google_search(query)
        try:
            # for i in search(query, tld="co.in", num=10, stop=10, pause=2):
            for i in search(query):
                print("search value:\t", search(i))
                # result = default_apps.google_search(query)
                Engine.Speak('Find some results in Google, Here it is. ')
                return webbrowser.open(i)
        except:
            Engine.Speak('Not Able to find out the query. ')
            pass

    def get_today(self):
        logging.debug(f'Initiate Day operation details from common features. ')
        day = datetime.datetime.today().weekday() + 1

        # this line tells us about the number
        # that will help us in telling the day
        day_dict = {1: 'Monday', 2: 'Tuesday',
                    3: 'Wednesday', 4: 'Thursday',
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}

        if day in day_dict.keys():
            day_of_the_week = day_dict[day]
            return Engine.Speak(f"Today is {day_of_the_week}")

    def tell_time(self):
        logging.debug(f'Initiate Time operation details from common features. ')
        time = str(datetime.datetime.now())

        # the time will be displayed like
        # this "2020-06-05 17:50:14.582630"
        # nd then after slicing we can get time
        print(time)
        hour = time[11:13]
        mins = time[14:16]
        return Engine.Speak(f"The time is {hour}Hours and{mins}minutes")

    def wikipedia_search(self, query):
        logging.debug(f'Initiate Wikipedia search operation. ')
        Engine.Speak("Checking the wikipedia ")
        # query = query.replace("wikipedia", "")
        query = self.qry_filter(qry=query, replace_str=['from wikipedia', 'in wikipedia'])
        result = wikipedia.summary(query, sentences=4)

        # TODO: Adding more module for User preference during communicate with Assistance.
        # Engine.Speak("According to wikipedia")
        # Engine.Speak(result)

        return webbrowser.open(result)

    def name_intro(self):
        logging.debug(f'Initiate Greeting operation. ')
        return Engine.Speak("I am Vani. Your Virtual Assistant")

    def play_music(self, query):
        logging.debug(f'Initiate music from youtube feature. ')
        try:
            query_song = self.qry_filter(query, ['play song', 'find song', 'play music'])
            pywhatkit.playonyt(query_song)
        except:
            Engine.Speak('repeat the song name again')

    def make_note(self): # Fixme: Note file is not creating. Need correction.
        logging.debug(f'Initiate Making note features. ')
        note_list = []
        Engine.Speak('Appending into existing file, please start after 2 sec')
        sleep(2)
        Engine.Speak('What should be the note Name:')
        get_file_name = Engine.take_command()
        print(f'get_file_name:\t{get_file_name}')
        Engine.Speak('What Shall be the content of the note')
        get_note_content = Engine.take_command()
        note_list.append(get_file_name)
        note_list.append(get_note_content)
        print(f'Note testing:\t{note_list}')
        Engine.Speak('Note creation completed>>>')

    def open_window(self):
        logging.debug(f'Initiate Open all open application switcher window. ')
        Engine.Speak('All the window app are here')
        return pa.hotkey('win', 'Tab')

    def open_app(self):  # Fixme: Application list name sort out & match with voice command.
        logging.debug(f'Initiate Specific app features. ')
        programs_list = ['pycharm',
                         'chrome', 'notepad',
                         'notepad++', 'outlook', 'teams',
                         'skype', 'slack', 'word', 'explorer',
                         'edge', 'firefox', 'cmd.exe']

        app_name = ''
        get_app_name = Engine.take_command()
        for i in range(len(programs_list)):
            app_name = programs_list[i]
            print(f'APP NAME:\t{app_name}')
            try:
                while True:
                    window_title = pa.getWindowsWithTitle(app_name)
                    window_title.activate()
                    break
            except:
                while True:
                    window = pa.getWindow(app_name)
                    if window:
                        window.set_foreground()
                        break

    def wake_up_cmd(self): # Fixme: Not properly synced with
        logging.debug(f'Initiate wake up keyword function for Virtual assistant. ')
        Engine.Speak('Vani is up for you!!')


com_feat = CommonFeatures()
