
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

    # for all searchable fields, items that are str
    def get_value(self, item):
        if self.field == "movie_name":
            return item.movie_name
        elif self.field == "genre":
            return item.genre
        elif self.field == "director":
            return item.director
        elif self.field == "production_company":
            return item.production_company
        elif self.field == "quote":
            return item.quote
        

    def insert(self, item):
        value = self.get_value(item)
        key = hashFunction(value)
        index = key % TABLE_SIZE

        #Simular insert logic to hash hw, but using nested lists incase of duplicates to prevent collisions.
        while True:
            # if the index is empty is sets the nested list equal to the index
            if self.table[index] == None:
                self.table[index] = [item]
                return
            # if the dex is occupied, but is a duplicate, it appends it to the nested list
            if self.get_value(self.table[index][0]) == value:
                self.table[index].append(item)
                return
            index = (index + 1) % TABLE_SIZE
    # essentually the same logic as the insert, but returns the index the given value is at
    def search(self, value):
        key = hashFunction(value)
        index = key % TABLE_SIZE

        while self.table[index] != None:
            if self.get_value(self.table[index][0]) == value:
                return self.table[index]
            index = (index + 1) % TABLE_SIZE
        return "Value not found"
    
    #simular logic to the previous two functions, it looks for the object at the index, even if there is multiple items in the index (duplicates) it deletes the specific object not just the first at index
    def delete(self, item):
        value = self.get_value(item)
        key = hashFunction(value)
        index = key % TABLE_SIZE

        while self.table[index] != None:
            # checks the index for the object then removes it, if it was the only one at index, it sets the index to None
            if item in self.table[index]:
                self.table[index].remove(item)
                if len(self.table[index]) == 0:
                    self.table[index] = None
                return
            index = (index + 1) % TABLE_SIZE
        return "Value not found"
