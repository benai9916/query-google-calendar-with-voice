# query-google-calendar-with-voice
This is a simple yet usefull voice assistant that enable you to check all the events from you google calendar.
It will list out as well as read out all the event for you along with the event time and date.

Only present and future event can be checked, there is no option to check the past events.

## Getting started
To use the google calendar we need to enable the google canlendar API and get the Auth click [here](https://developers.google.com/calendar/quickstart/python)  

-> click on `enable the google calendar API` and follow the setps to set up. 

-> click on `download client configuration` and place the credentials.json to you porject root folder. 

-> run below command
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
```
pip install -r requirements.txt
```

-> cd into your working directory and run
```
python mainVoice.py
```
-> If you run `mainVoice.py` for the firs time it will redirect you to the browser for authentication, please click on the link and verify

-> To trigger/initialize the voice assistant speak `hi mario`

-> To quit the voice assistant speak 'thank you`

### That's all folks.
