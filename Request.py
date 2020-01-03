import requests
from bs4 import BeautifulSoup
from DataPayload import login_data, payload


def get_table():
    url = 'https://{}:{}@intra.tsi.lv/root/StudentsDatabase1/?page=4'.format(login_data['username'],
                                                                             login_data['password'])
    with requests.session() as session:
        soup = BeautifulSoup(session.post(url=url, data=payload, verify=False).content, 'html5lib')
        attributes = {
            'class': 'main_table',
            'style': 'width:690px;margin-top:10px;margin-bottom:20px;margin-left:0px;padding:0px;'
        }

        return soup.find('table', attrs=attributes).find('tbody')


class Request:
    def __init__(self):
        self.table = get_table()
        self.rows = self.table.find_all('tr')
        self.headers = self.get_headers()

    def get_data_text(self):
        for data_text in self.get_data():
            yield data_text

    def get_data(self):
        for data in self.get_row():
            yield data

    def get_row(self):
        for row in self.rows:
            yield row

    def get_headers(self):
        for row in self.rows:
            return row.find_all('th')
