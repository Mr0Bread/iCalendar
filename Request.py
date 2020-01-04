import requests
from bs4 import BeautifulSoup
from DataPayload import login_data, payload
import re


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
        self.print_data_list()

    def get_headers(self):
        for row in self.rows:
            return row.find_all('th')

    def print_data_list(self):
        tmp_list = []
        data_list = []
        regex = re.compile('[\t\n]')

        for row in self.rows:

            for cell in row.find_all('td'):
                tmp_list.append(regex.sub('', str(cell.text)))

            data_list.append(tmp_list)
            tmp_list = []
        data_list.pop(0)
        print(data_list)
