from datetime import datetime


def get_day():
    return str(datetime.now().day)


def get_month():
    month = datetime.now().month

    if 0 < month < 10:
        return '0' + str(month)


def get_year():
    return str(datetime.now().year)
