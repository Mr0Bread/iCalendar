import json
from Request import Request


class JSONExporter(Request):
    def __init__(self):
        super().__init__()
        self.request = Request()


    def export_to_json(self):
        with open('Schedule.json', mode='w') as json_file:
            value_for_exporting = []
            data_for_exporting = {}
            

