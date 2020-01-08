from datetime import datetime
from TimeGetter import get_day, get_month, get_year

login_data = {
        'username': 'st75084',
        'password': 'Elishka1Love'
    }

payload = {
        'AfterForm': '1',
        'idSession': 'c3704d48a250ad3b6f39e03eb92ce529',
        'dt1': get_day(),
        'mn1': get_month(),
        'yr1': get_year(),
        'dt2': '1',
        'mn2': '07',
        'yr2': '2020',
        'idStudentGroup': '1420',
        'idLecturer': '0',
        'idApartment': '0'
    }