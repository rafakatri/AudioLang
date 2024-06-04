
class Symbol_Table:
    
    def __init__(self):
        self.table = {}

    def get_value(self, key):
        if key in self.table.keys():
            return self.table[key]
        raise Exception('ID nao existe')
    
    def exists_key(self, key):
        return key in self.table.keys()

    def set_value(self, key, value):
        self.table[key] = value
