# COS226_Final_Project_Bruce_Bossow

This database system runs via python main.py with an interactive menu that guides users through loading CSV data, creating indexes on numeric fields (rating, revenue, etc.), performing exact searches on string fields (director, genre, etc.), executing range queries, exporting results to CSV, and deleting records. For example, after loading data, you might create an index on "rating" with create index rating, then search for films rated 7.5-9.0 with range search rating 7.5 9.0, which would return matching movies and allow export or deletion.

The system's hash tables use a multiplicative hash function with prime number 31 for good distribution, while B+ trees (max degree 5) enable efficient range scans through linked leaf nodes. I chose searchable fields based on data strings for exact hashing (movie_name, director) and ints/floats for range indexing (release_date, revenue). Efficiency varies: initialization is O(n) per hash table, index creation is O(n log n) for sorting, queries are O(1) average for exact and O(log n + k) for range, and deletions maintain consistency across all structures. Known limitations include fixed hash table size (15073), Only supports specific numeric fields for range queries, and Database exists only in memory during runtime.

Controls:

LOAD (doesnt need anything else)

CREATE_INDEX rangeField

PRINT_INDEX (requires nothing, prints your current list of indexes)

SEARCH SearchField searchible (the searchible would be watch your searching for in the specific field)

RANGE rangeField Low High (if you want between two bounds you'd fill low and high with nums, for less than you'd put None in for low and for greater than youd put None in for high)

EXPORT (doesnt need anything else, automatically writes your most recent search into results.csv)
(This only exports your most recent search, any prior wont be written, if you export again your previous export will be overwritten and lost)

DELETE (Requires nothing, deletes your most recent search from indexes)

QUIT (requires nothing, quits out of the loop)