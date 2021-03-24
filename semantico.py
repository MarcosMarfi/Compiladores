class Semantico:
    TABLE_SIMBLE = {}

    def __init__(self, id):
        self.id = id

    def add(self, element):
        if element['id'] in Semantico.TABLE_SIMBLE:
            raise Exception(element+" already exists!")
            return False
        self.TABLE_SIMBLE[element['id']] = element

    def get(self, element):
        for id, data in Semantico.TABLE_SIMBLE.items():
            if data['id'] == element:
                return data
        return None