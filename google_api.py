from __future__ import print_function

import csv
import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar():
    """
    This function connects the python program to the Google Calendar
    of the user
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_events(x):
    """
    This function gets the events for a particular day from the calendar
    :param x: The day to be checked
            x => int 0 -> today
                     1 -> tomorrow
                     -1 -> yesterday ...
    """
    # Call the Calendar API
    service = get_calendar()

    now = (datetime.datetime.now() - datetime.timedelta(days=(1 - x))).isoformat() + 'Z'  # 'Z' indicates UTC time
    now = now[:11] + '18:30:00.000000Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=50, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    todayData = []

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        stop = event['end'].get('dateTime', event['start'].get('date'))
        date = start[:10]
        starttime = start[11:16]
        stoptime = stop[11:16]
        if date == str(datetime.date.today() + datetime.timedelta(days=x)):
            # print(event['summary'])
            todayData.append([date, starttime, stoptime, event['summary']])
        else:
            break

    return todayData

def create_events(event):
    """
    This function creates events in the Google Calendar
    :param event: Event to be added
            Should be of the form [start, end, eventName]
            start, end => string, 'year-month-day hour:min:sec.msec'
            eventName => string
    """
    # event should be a list like [start, end, eventName]
    service = get_calendar()
    start = datetime.datetime.strptime(event[0], '%Y-%m-%d %H:%M:%S.%f').isoformat()
    end = datetime.datetime.strptime(event[1], '%Y-%m-%d %H:%M:%S.%f').isoformat()

    event_result = service.events().insert(
        calendarId='primary',
        body={
            "summary": event[2],
            "description": 'This event was automatically added by THE AUTO CALENDAR SCHEDULER',
            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
            'colorId': '4',
        },
    ).execute()
    return event_result


def timeformater(t):
    if t[0] == '0':
        t = int((t[1:2] + t[3:]))
    else:
        t = int((t[:2] + t[3:]))
    return t


def slotter(tdata):
    """
    This function places all the events into a csv
    """
    with open('Times.csv', 'r') as sched:
        cr = csv.reader(sched)
        lst = [i for i in cr]
    for event in tdata:
        if not event[1]:
            continue
        t1 = timeformater(event[1])
        t2 = timeformater(event[2])
        for i in lst:
            h = timeformater(i[0])
            try:
                if t1 <= h < t2:
                    i[1] = event[3]
            except:
                print('alert')
                print(t1, type(t1), type(t2), type(h))
    with open('daySchedule.csv', 'w') as sched:
        cw = csv.writer(sched)
        cw.writerows(lst)


def unslotter(m):
    """
    This function takes all the events from a csv and puts it into the calendar
    """
    date = str(datetime.date.today() + datetime.timedelta(days=m))

    with open('updayschedule.csv', 'r') as sched:
        cr = csv.reader(sched)
        events = [i for i in cr if i not in [ [], ['', ''] ]]

    for i in range(len(events)):
        if events[i][1] != "None":
            if events[i][1] != events[i - 1][1]:
                startTime = date + ' ' + events[i][0] + ':00.0'

            try:
                if events[i + 1][1] != events[i][1]:
                        endTime = date + ' ' + events[i + 1][0] + ':00.0'
                        create_events([startTime, endTime, events[i][1]])
            except:
                endTime = date + ' ' + '23:59' + ':00.0'
                create_events([startTime, endTime, events[i][1]])


# get_events(0)
# slotter(get_events(0))
# unslotter(0)
# create_events(['2021-01-15 15:00:00.0', '2021-01-15 16:00:00.0', 'woah'])
