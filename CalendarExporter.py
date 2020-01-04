from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from os.path import isfile
from googleapiclient.discovery import build
from datetime import timedelta, datetime
from Request import Request


def create_credentials():
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=scopes)

    if not isfile('token.pkl'):
        print('creating token')

        with open('token.pkl', mode='wb') as file:
            pickle.dump(flow.run_console(), file)

    return pickle.load(open('token.pkl', mode='rb'))


class CalendarExporter:
    def __init__(self):
        self.setup_oauth()
        self.get_calendar()
        self.calendar_id = self.get_calendar_id()
        self.request = Request()

    def setup_oauth(self):
        credentials = create_credentials()
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar(self):
        self.calendar = self.service.calendarList().list().execute()

    def get_calendar_id(self):
        return self.calendar['items'][0]['id']

    def get_events(self):
        self.events = self.service.events().list(calendarId=self.calendar_id, timeZone='Europe/Riga').execute()

    def create_event(self):
        start_time = datetime(2020, 1, 6, 13, 30, 0)
        end_time = start_time + timedelta(hours=2)
        time_zone = 'Europe/Riga'

        event = {
            'summary': 'IPL Final 2019',
            'location': 'Riga',
            'description': 'Testing events',
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
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
