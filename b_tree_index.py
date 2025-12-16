from b_tree import BTree

class BTreeIndex:
    def __init__(self, field):
        self.field = field
        self.tree = BTree(maxdegree = 5)

    # Index fields, any input that is an int/float
    def get_value(self, item):
        if self.field == "release_date":
            return item.release_date
        elif self.field == "revenue":
            return item.revenue
        elif self.field == "rating":
            return item.rating
        elif self.field == "min_duration":
            return item.min_duration
        
    

    # Uses btree remove function to remove values.
    def delete(self, item):
        self.tree.remove(self.get_value(item))