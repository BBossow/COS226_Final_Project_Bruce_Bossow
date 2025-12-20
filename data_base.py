# This is the main database where the btree and hash table are connected to

from hash_table import HashTable
from b_tree_index import BTreeIndex

class Database:
    def __init__(self):
        self.records = []
        self.last_results = []

        self.hash_tables = {
            "movie_name": HashTable("movie_name"),
            "genre": HashTable("genre"),
            "director": HashTable("director"),
            "production_company": HashTable("production_company"),
            "quote": HashTable("quote")
        }

        self.btree_indexes = {}

    def creation(self, records):
        self.records = records
        for item in records:
            for table in self.hash_tables.values():
                table.insert(item)

    def create_index(self, field):
        index = BTreeIndex(field)
        index.build(self.records)
        self.btree_indexes[field] = index

    def print_index(self):
        for index in self.btree_indexes:
            print(index)

    def exact_search(self, field, value):
        self.last_results = self.hash_tables[field].search(value)
        return self.last_results
    
    def range_search(self, field, low, high):
        if field not in self.btree_indexes:
            print("Field not indexed")
            return []
        self.last_results = self.btree_indexes[field].range_search(low, high)
        return self.last_results

    def delete_results(self):
        for item in self.last_results:
            self.records.remove(item)
            for table in self.hash_tables.values():
                table.delete(item)
            for index in self.btree_indexes.values():
                index.delete(item)
        self.last_results = []