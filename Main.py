from CalendarExporter import CalendarExporter


class Main:
    def __init__(self):
        self.calendar_exporter = CalendarExporter()


if __name__ == '__main__':
    main = Main()
    main.calendar_exporter.update_calendar()
