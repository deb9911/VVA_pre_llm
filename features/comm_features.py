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

import logging_config
from engine.engine_updated import engine as Engine
from features import default_apps
from time import strftime, sleep

# Set up the logger
log_dir = './logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
file_name = strftime("%Y-%m-%d") + '_CommonFeatures.logs'
filepath = os.path.join(log_dir, file_name)

logging.basicConfig(filename=filepath, filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# logger = logging.getLogger(__name__)
logger = logging_config.get_logger(__name__)
logger.info(f'Logging started. Log file at: {filepath}')


# Common Features class
class CommonFeatures:

    # @staticmethod
    def qry_filter(self, qry: str, replace_str: list):
        logger.debug(f'Initiate Query filter operation. Query: {qry}, Replace: {replace_str}')
        if qry is not None:
            for r in range(len(replace_str)):
                qry = qry.replace(replace_str[r], "")
                logger.debug(f'Filtered Query: {qry}')
            return qry
        else:
            logger.info(f'Query is none: {qry}')
            Engine.Speak("Empty Query>>> ")

    def open_google(self):
        logger.debug('Initiate Open Google operation.')
        Engine.Speak("Opening Google ")
        return webbrowser.open("www.google.com")

    def google_search(self, query):
        logger.debug(f'Initiate Search content from Google operation. Query: {query}')
        Engine.Speak('Checking in Google')
        query = self.qry_filter(query, ['search in google', 'find from google'])
        try:
            for i in search(query):
                logger.debug(f'Google search result: {i}')
                Engine.Speak('Found some results in Google, here it is.')
                return webbrowser.open(i)
        except Exception as e:
            logger.error(f'Google search failed: {e}')
            Engine.Speak('Not able to find the query.')
            pass

    def google_search_helper(self, url):
        logger.debug(f'Initiate Google search helper operation. URL: {url}')
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            result = soup.get_text()

            interesting_lines = [line for line in result.split("\n") if len(line) > 30]
            logger.debug(f'Filtered lines from URL: {interesting_lines}')
            return interesting_lines
        except Exception as e:
            logger.error(f'Error in google_search_helper: {e}')
            return None

    def get_today(self):
        logger.debug('Initiate Day operation details from common features.')
        day = datetime.datetime.today().weekday() + 1

        day_dict = {1: 'Monday', 2: 'Tuesday',
                    3: 'Wednesday', 4: 'Thursday',
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}

        if day in day_dict.keys():
            day_of_the_week = day_dict[day]
            date_str = f"Today is {day_of_the_week}"
            logger.info(f'Today\'s day: {day_of_the_week}')
            return Engine.Speak(date_str)

    def tell_time(self):
        logger.debug('Initiate Time operation details from common features.')
        time_str = str(datetime.datetime.now())
        hour = time_str[11:13]
        mins = time_str[14:16]
        logger.info(f'Current time: {hour}:{mins}')
        return Engine.Speak(f"The time is {hour} hours and {mins} minutes")

    def wikipedia_search(self, query):
        logger.debug(f'Initiate Wikipedia search operation. Query: {query}')
        Engine.Speak("Checking Wikipedia")
        query = self.qry_filter(query, ['from wikipedia', 'in wikipedia'])
        try:
            result = wikipedia.summary(query, sentences=4)
            logger.debug(f'Wikipedia summary: {result}')
            return webbrowser.open(result)
        except Exception as e:
            logger.error(f'Wikipedia search failed: {e}')
            return Engine.Speak('Could not find any results on Wikipedia.')

    def name_intro(self):
        logger.debug('Initiate Greeting operation.')
        return Engine.Speak("I am Vani, your Virtual Assistant")

    def play_music(self, query):
        logger.debug(f'Initiate music from YouTube feature. Query: {query}')
        try:
            query_song = self.qry_filter(query, ['play song', 'find song', 'play music'])
            pywhatkit.playonyt(query_song)
        except Exception as e:
            logger.error(f'Error playing music: {e}')
            Engine.Speak('Please repeat the song name.')

    def make_note(self):
        logger.debug('Initiate making note features.')
        note_list = []
        Engine.Speak('Please start after 2 seconds to append into an existing file.')
        sleep(2)
        Engine.Speak('What should be the note name?')
        get_file_name = Engine.take_command()
        logger.info(f'Note name: {get_file_name}')
        Engine.Speak('What should be the content of the note?')
        get_note_content = Engine.take_command()
        logger.info(f'Note content: {get_note_content}')
        note_list.append(get_file_name)
        note_list.append(get_note_content)
        Engine.Speak('Note creation completed.')

    def switch_window_by_title(self, title):
        logger.debug(f'Switching window by title: {title}')
        try:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                window = windows[0]
                window.activate()
                logger.info(f'Switched to window with title: {title}')
                return f"Switched to window with title: {title}"
            else:
                logger.warning(f'No window found with title: {title}')
                return f"No window found with title: {title}"
        except Exception as e:
            logger.error(f'Error switching to window by title: {e}')
            return f"Error switching to window with title {title}: {str(e)}"

    def switch_window_by_id(self, window_id):
        logger.debug(f'Switching window by ID: {window_id}')
        try:
            window = gw.getWindowsAt(window_id)
            if window:
                window.activate()
                logger.info(f'Switched to window with ID: {window_id}')
                return f"Switched to window with ID: {window_id}"
            else:
                logger.warning(f'No window found with ID: {window_id}')
                return f"No window found with ID: {window_id}"
        except Exception as e:
            logger.error(f'Error switching to window by ID: {e}')
            return f"Error switching to window with ID {window_id}: {str(e)}"

    def list_open_windows(self):
        logger.debug('Listing all open windows.')
        windows = gw.getAllTitles()
        logger.info(f'Open windows: {windows}')
        return windows

    # def open_window(self, window_title):
    #     logger.debug(f'Attempting to open window with title: {window_title}')
    #     pa.hotkey('win', 'Tab')
    #     time.sleep(1)  # Wait for the window switcher to open
    #
    #     def enum_window_titles(hwnd, results):
    #         if win32gui.IsWindowVisible(hwnd):
    #             results.append(win32gui.GetWindowText(hwnd))
    #
    #     windows = []
    #     win32gui.EnumWindows(enum_window_titles, windows)
    #
    #     for i, title in enumerate(windows):
    #         if window_title.lower() in title.lower():
    #             for _ in range(i):
    #                 pa.press('down')
    #                 time.sleep(0.1)
    #             pa.press('enter')
    #             logger.info(f'Switched to window with title: {window_title}')
    #             return
    #
    #     pa.hotkey('esc')  # Exit the window switcher
    #     logger.warning(f"Could not find a window with the title {window_title}.")
    #     Engine.Speak(f"Could not find a window with the title {window_title}.")

    def open_window(self):
        logging.debug(f'Initiate Open all open application switcher window. ')
        Engine.Speak('All the window app are here')
        return pa.hotkey('win', 'Tab')

    def open_app(self):
        logger.debug('Initiate open specific app feature.')
        programs_list = ['pycharm', 'chrome', 'notepad', 'notepad++', 'outlook',
                         'teams', 'skype', 'slack', 'word', 'explorer', 'edge',
                         'firefox', 'cmd.exe']

        get_app_name = Engine.take_command()
        logger.info(f'Application to open: {get_app_name}')
        for app_name in programs_list:
            try:
                while True:
                    window_title = pa.getWindowsWithTitle(app_name)
                    window_title.activate()
                    break
            except Exception as e:
                logger.error(f'Error opening application {app_name}: {e}')

    def wake_up_cmd(self):
        logger.debug('Initiate wake up keyword function for Virtual assistant.')
        Engine.Speak('Vani is up for you!!')


# Initialize an instance of CommonFeatures
com_feat = CommonFeatures()
