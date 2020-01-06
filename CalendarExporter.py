from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from os.path import isfile
from googleapiclient.discovery import build
from datetime import timedelta, datetime
from Request import Request

TSI = 'Институт транспорта и связи, Lomonosova iela 1, Latgales priekšpilsēta, Rīga, LV-1019, Латвия'


def create_credentials():
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=scopes)

    if not isfile('token.pkl'):
        print('creating token')

        with open('token.pkl', mode='wb') as file:
            pickle.dump(flow.run_console(), file)

    return pickle.load(open('token.pkl', mode='rb'))


def get_lesson_description(lesson):
    lecturer = lesson[5]
    lesson_number = lesson[1]

    return 'Пара: {}\nВедет: {}'.format(lesson_number, lecturer)


def get_lesson_title(lesson):
    return lesson[6]


def get_lesson_start_time(lesson):
    # datetime(2020, 1, 6, 13, 30, 0)

    date = lesson[0].rsplit('.')

    day = date[0]
    if day[0] == '0':
        day = day[1]
    day = int(day)

    month = date[1]
    if month[0] == '0':
        month = month[1]
    month = int(month)

    year = int(date[2])
    date = lesson[2]
    start_time = date.rsplit('-')
    start_time = start_time[0].rsplit(':')
    start_hour = int(start_time[0])
    start_minute = int(start_time[1])
    start = datetime(year, month, day, start_hour, start_minute, 0)
    return start


class CalendarExporter:
    def __init__(self):
        self.setup_oauth()
        self.get_calendar()
        self.calendar_id = self.get_calendar_id()
        self.request = Request()
        self.fill_calendar()

    def setup_oauth(self):
        credentials = create_credentials()
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar(self):
        self.calendar = self.service.calendarList().list().execute()

    def get_calendar_id(self):
        return self.calendar['items'][0]['id']

    def get_events(self):
        self.events = self.service.events().list(calendarId=self.calendar_id, timeZone='Europe/Riga').execute()
        print(self.events)

    def create_event(self, lesson):
        time_zone = 'Europe/Riga'
        title = get_lesson_title(lesson)

        start_time = get_lesson_start_time(lesson)
        end_time = start_time + timedelta(hours=1, minutes=30)
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")

        description = get_lesson_description(lesson)

        event = {
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

        self.service.events().insert(calendarId=self.calendar_id, body=event).execute()

    def fill_calendar(self):
        for lesson in self.request.get_data_list():
            self.create_event(lesson)
