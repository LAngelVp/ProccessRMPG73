import json
from .Logica_Reportes.Variables.ContenedorVariables import Variables
class CreateJson(Variables):
    def __init__(self, route=None):
        if route is None:
            self.route_document = Variables().movement_date_document
        else:
            self.route_document = route
    # Create Json with new date
    def update_date(self, new_date):
        #comment create json
        data = { "Date_Movement" : [new_date]}
        #comment Update Json
        with open(self.route_document, "w") as json_file:
            new_data = json.dump(data, json_file, indent=4)
