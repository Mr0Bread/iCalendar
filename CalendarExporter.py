from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from os.path import isfile
from googleapiclient.discovery import build


class CalendarExporter:
    def __init__(self):
        self.setup_oauth()
        self.get_calendar()

    def setup_oauth(self):
        credentials = self.create_credentials()
        self.service = build('calendar', 'v3', credentials=credentials)

    def create_credentials(self):
        scopes = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=scopes)

        if not isfile('token.pkl'):
            print('creating token')

            with open('token.pkl', mode='wb') as file:
                pickle.dump(flow.run_console(), file)

        return pickle.load(open('token.pkl', mode='rb'))

    def get_calendar(self):
        print(self.service.calendarList().list().execute())
