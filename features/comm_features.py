import os
import sys
import webbrowser
import wikipedia
import pywhatkit
import pyautogui as pa
import datetime
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import logging
import pygetwindow as gw
import time
import win32gui

from engine.engine_updated import engine as Engine
from features import default_apps
from time import strftime, sleep


# dr = webdriver.Chrome()


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
        # print(f'Unfiltered Query:\t{query}')
        query = self.qry_filter(query, ['search in google', 'find from google'])
        # print(f'Filtered query:\t{query}')
        # content = google_search(query)
        try:
            # for i in search(query, tld="co.in", num=10, stop=10, pause=2):
            for i in search(query):
                print("search value:\t", search(i))
                # read_out_content = self.google_search_helper(i)
                Engine.Speak('Find some results in Google, Here it is. ')
                # Engine.Speak(read_out_content)

                return webbrowser.open(i)
        except:
            Engine.Speak('Not Able to find out the query. ')
            pass

    def google_search_helper(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        # soup = BeautifulSoup(response.page_source, "lxml")
        result = soup.get_text()

        interesting_lines = [line for line in result.split("\n") if len(line) > 30]
        print(f'result\t{interesting_lines}')
        return interesting_lines

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
            date_str = f"Today is {day_of_the_week}"
            return Engine.Speak(date_str)

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

    def switch_window_by_title(self, title):
        try:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                window = windows[0]
                window.activate()
                return f"Switched to window with title: {title}"
            else:
                return f"No window found with title: {title}"
        except Exception as e:
            return f"Error switching to window with title {title}: {str(e)}"

    def switch_window_by_id(self, window_id):
        try:
            window = gw.getWindowsAt(window_id)
            if window:
                window.activate()
                return f"Switched to window with ID: {window_id}"
            else:
                return f"No window found with ID: {window_id}"
        except Exception as e:
            return f"Error switching to window with ID {window_id}: {str(e)}"

    def list_open_windows(self):
        windows = gw.getAllTitles()
        return windows

    # def open_window(self, window_title=None):
    #     logging.debug(f'Initiate Open all open application switcher window.')
    #
    #     if window_title:
    #         result = self.switch_window_by_title(window_title)
    #         Engine.Speak(result)
    #     else:
    #         Engine.Speak('All the window app are here')
    #         pa.hotkey('win', 'Tab')

    def open_window(self, window_title):
        # Press 'win' + 'Tab' to open the window switcher
        pa.hotkey('win', 'Tab')
        time.sleep(1)  # Wait for the window switcher to open

        # List all window titles
        def enum_window_titles(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                results.append(win32gui.GetWindowText(hwnd))

        windows = []
        win32gui.EnumWindows(enum_window_titles, windows)

        # Search for the specified window title
        for i, title in enumerate(windows):
            if window_title.lower() in title.lower():
                # Simulate pressing the down arrow to navigate to the desired window
                for _ in range(i):
                    pa.press('down')
                    time.sleep(0.1)

                # Press 'Enter' to focus on the selected window
                pa.press('enter')
                return

        # If no matching window found, speak an error message
        pa.hotkey('esc')  # Exit the window switcher
        Engine.Speak(f"Could not find a window with the title {window_title}.")

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
