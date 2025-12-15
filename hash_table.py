
TABLE_SIZE = 15073 #Consant

# Hash function for Hash table, used my best function from homework
def hashFunction(stringData):
    # takes the unicode for each char in string data, multiplies by a set number, then adds key
    key  = 0
    for char in stringData:
        # takes the unicode for each char to make the key
        key = ord(char) * 31 + key

    return key 


class HashTable:
    def __init__(self, field):
        self.field = field
        self.table = [None] * TABLE_SIZE