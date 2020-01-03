from JSONExporter import JSONExporter
from CalendarExporter import CalendarExporter


class Main(JSONExporter, CalendarExporter):
    def __init__(self):
        super().__init__()
        self.calendar_exporter = CalendarExporter()


if __name__ == '__main__':
    main = Main()
