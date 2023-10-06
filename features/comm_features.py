import os
import sys
import webbrowser
import wikipedia
import pywhatkit
import pyautogui as pa
import datetime
from googlesearch import search

from engine.engine import Engine
from features import default_apps
from time import strftime, sleep


class CommonFeatures:
    @staticmethod
    def qry_filter(qry: str, replace_str: list):
        if qry is not None:
            for r in range(len(replace_str)):
                print(f'Qry from Common Features:\t{qry}')
                qry = qry.replace(replace_str[r], "")
                return qry
        else:
            Engine.Speak("Empty Query>>> ")

    def open_google(self):
        Engine.Speak("Opening Google ")
        return webbrowser.open("www.google.com")

    def google_search(self, query):
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
                # return webbrowser.open(search(i))
                return webbrowser.open(i)
                # return i
        except:
            Engine.Speak('Not Able to find out the query. ')
            pass

    def get_today(self):
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

        time = str(datetime.datetime.now())

        # the time will be displayed like
        # this "2020-06-05 17:50:14.582630"
        # nd then after slicing we can get time
        print(time)
        hour = time[11:13]
        mins = time[14:16]
        return Engine.Speak(f"The time is {hour}Hours and{mins}minutes")

    def wikipedia_search(self, query):
        Engine.Speak("Checking the wikipedia ")
        # query = query.replace("wikipedia", "")
        query = self.qry_filter(qry=query, replace_str=['from wikipedia', 'in wikipedia'])
        result = wikipedia.summary(query, sentences=4)

        # TODO: Adding more module for User preference during communicate with Assistance.
        # Engine.Speak("According to wikipedia")
        # Engine.Speak(result)

        return webbrowser.open(result)

    def name_intro(self):
        return Engine.Speak("I am Vani. Your Virtual Assistant")

    def play_music(self, query):
        try:
            query_song = self.qry_filter(query, ['play song', 'find song', 'play music'])
            pywhatkit.playonyt(query_song)
        except:
            Engine.Speak('repeat the song name again')

    def make_note(self):
        note_list = []
        Engine.Speak('Appending into existing file, please start after 2 sec')
        sleep(2)
        Engine.Speak('What should be the note Name:')
        get_file_name = Engine.take_command().lower()
        Engine.Speak('What Shall be the content of the note')
        get_note_content = Engine.take_command().lower()
        note_list.append(get_file_name)
        note_list.append(get_note_content)
        print(f'Note testing:\t{note_list}')
        Engine.Speak('Note creation completed>>>')

    def open_window(self):
        Engine.Speak('All the window app are here')
        return pa.hotkey('win', 'Tab')

    def wake_up_cmd(self):
        Engine.Speak('Vani is up for you!!')


com_feat = CommonFeatures()
