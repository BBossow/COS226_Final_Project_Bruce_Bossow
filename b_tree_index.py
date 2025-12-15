from b_tree import BTree

class BTreeIndex:
    def __init__(self, field):
        self.field = field
        self.tree = BTree(maxdegree = 5)