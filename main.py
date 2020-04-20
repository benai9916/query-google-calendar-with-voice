from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
import time
import playsound
import speech_recognition as sr
import pyttsx3
import pytz
import subprocess
from gtts import gTTS
 
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

def speak(text):
    # take the text and the language will be english
    text = gTTS(text=text, lang="en")
    # save the audio file in mp3 formate
    filename = "voice.mp3"
    # save the file, will be save in the project root directory 
    text.save(filename)
    # play the txt as a audio 
    playsound.playsound(filename)

# listen the voice command and return it in a string formate
def get_audio():
    # create a Recognizer object
    recognise = sr.Recognizer()
    # listen to the microphone
    with sr.Microphone() as source:
        # listent to the audio
        audio = recognise.listen(source)
        said = ""

        try:
            # use google recognizer to process the audio
            said = recognise.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
        
    return said.lower()

def authenticate_calender():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # google canlender credentials will be save in the project root folder
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run, it will be save in the poject root folder
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day, service):
    # formating the start date and end date
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    # covert the time into UTC formate
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    # Call the calender API
    events_result = service.events().list(calendarId='primary', 
                                        timeMin=date.isoformat(),
                                        timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        # sepak out the number of event available on that particular day
        speak(f"you have {len(events)} events on this day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

            # Spliting the time into readable formate
            start_time = str(start.split('T')[1].split('+')[0])
            if int(start_time.split(':')[0]) < 12:
                start_time = start_time.split(':0')[0] + 'am'
            else:
                start_time = str(int(start_time.split(':')[0]) - 12)
                start_time = start_time.split(':0')[0] + 'pm'

            # speaking out the events summary along with the events time
            speak(str(event['summary']) + 'at' + start_time)

# check and process the text to get the events from calender
def get_date(text):
    text = text.lower()
    # create date time object
    today = datetime.date.today()

    # if text contain the word today then return today's date
    if text.count('today') > 0:
        return today 
    
    day = -1
    day_of_week =-1
    month = -1
    year = today.year

     # Split the text by empty space
    for word in text.split():
        # if txt contain the word 'month' check the month in the list of monthe and get the index and increament by 1
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        # if text contain word like 5th or 6th, seperate the number from letter
                        day = int(word[:found])
                    except: 
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if day < today.day and month == -1 and day != -1:
        month =  month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_the_week = today.weekday()
        dif = day_of_week - current_day_of_the_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if month == -1 or day == -1:
        return None
    else:
        return datetime.date(month=month, day=day, year=year)    

# trigger the voice assistance with 'hi mario'
WAKE = 'hi mario'
SERVICE = authenticate_calender()

while True:
    print('listening..')
    trigger_assistant = get_audio()

    # if trigger_assistant contain 'hi mario' then activate the voice assistant
    if trigger_assistant.count(WAKE) > 0:
        speak('I am listening')

        text = get_audio()
        # get the date from the get_date function
        date = get_date(text)
        if date:
            get_events(date, SERVICE)
        elif text.count('thank you') > 0:
            speak('anytime! bye')
            break
        else:
            print('Please try again with valid sentence')

    # on saying thank you terminate the voice assistant
    else:
        if trigger_assistant.count('thank you') > 0:
            speak('anytime! bye')
            break