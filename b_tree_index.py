# This is where btree is controlled

from b_tree import BTree
from quicksort import QuickSort

class BTreeIndex:
    def __init__(self, field):
        self.field = field
        self.tree = BTree(5, field)

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

        
    def build(self, records):
        sorter = QuickSort()
        sortedItems = sorter.quickSort(records, self.field)
        self.tree.bulk_load(sortedItems)

    def range_search(self, low, high):
        return self.tree.range_search(low, high)

    # Uses btree remove function to remove values.
    def delete(self, item):
        self.tree.remove(self.get_value(item))