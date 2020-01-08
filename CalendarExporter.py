from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from os.path import isfile
from googleapiclient.discovery import build
from datetime import timedelta, datetime
from Request import Request
from time import sleep
import json

TSI = 'Институт транспорта и связи, Lomonosova iela 1, Latgales priekšpilsēta, Rīga, LV-1019, Латвия'


def create_credentials():
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=scopes)

    if not isfile('token.pkl'):
        print('creating token')

        with open('token.pkl', mode='wb') as file:
            pickle.dump(flow.run_console(), file)

    return pickle.load(open('token.pkl', mode='rb'))


def get_lesson_description(lesson_data):
    return 'Пара: {}\nВедет: {}\nАудитория: {}\nВид: {}\nПримечание: {}'.format(lesson_data[1], lesson_data[5],
                                                                                lesson_data[3],
                                                                                lesson_data[7], lesson_data[8])


def get_lesson_title(lesson_data):
    return lesson_data[6]


def get_lesson_start_time(lesson_data):
    # datetime(2020, 1, 6, 13, 30, 0)

    date = lesson_data[0].rsplit('.')

    day = date[0]
    if day[0] == '0':
        day = day[1]
    day = int(day)

    month = date[1]
    if month[0] == '0':
        month = month[1]
    month = int(month)

    year = int(date[2])
    date = lesson_data[2]
    start_time = date.rsplit('-')
    start_time = start_time[0].rsplit(':')
    start_hour = int(start_time[0])
    start_minute = int(start_time[1])

    return datetime(year, month, day, start_hour, start_minute, 0)


def get_event_body(lesson_data):
    time_zone = 'Europe/Riga'
    title = get_lesson_title(lesson_data)

    start_time = get_lesson_start_time(lesson_data)
    end_time = start_time + timedelta(hours=1, minutes=30)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    description = get_lesson_description(lesson_data)

    return {
        'summary': title,
        'location': TSI,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': time_zone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }


class CalendarExporter:
    def __init__(self):
        self.setup_oauth()
        self.get_calendar()
        self.calendar_id = self.get_calendar_id()
        self.request = Request()
        self.fill_calendar()
        self.export_events_from_calendar_to_json()
        self.update_calendar()

    def setup_oauth(self):
        credentials = create_credentials()
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar(self):
        return self.service.calendarList().list().execute()

    def get_calendar_id(self):
        return self.get_calendar()['items'][0]['id']

    def get_events(self):
        return self.service.events().list(calendarId=self.calendar_id, timeZone='Europe/Riga').execute()

    def export_events_from_calendar_to_json(self):
        with open('events.json', mode='w') as file:
            json.dump(self.get_events(), file, indent=4)

    def create_event(self, lesson_data):
        self.service.events().insert(calendarId=self.calendar_id, body=get_event_body(lesson_data)).execute()

    def fill_calendar(self):
        if self.is_calendar_not_filled():
            for lesson_data in self.request.get_lesson_list():
                self.create_event(lesson_data)

    def clear_calendar(self):
        self.service.calendars().clear(calendarId=self.calendar_id).execute()

    def is_calendar_not_filled(self):
        try:
            self.get_events()['items'][0]
        except IndexError:
            return True

    def update_calendar(self):
        while True:
            self.request.update_schedule()
            sleep(3600)
            self.clear_calendar()
            self.fill_calendar()


