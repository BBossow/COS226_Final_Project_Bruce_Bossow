# This is where my text interface will be 

from data_base import Database
from loader import load_csv
from exporter import export_csv

db = Database()

while True:
    print()
    print("Range fields: release_date, revenue, rating, min_duration")
    print("Searchable fields: movie_name, genre, director, production_company, quote")
    print("Controls: ")
    print("LOAD, CREATE_INDEX, PRINT_INDEX, SEARCH, RANGE, EXPORT, DELETE, QUIT")
    cmd = input("> ").split()

    if cmd[0] == "LOAD":
        db.creation(load_csv("MOCK_DATA.csv"))
        print("Data loaded")

    elif cmd[0] == "CREATE_INDEX":
        db.create_index(cmd[1])
        print("Index created")

    elif cmd[0] == "PRINT_INDEX":
        db.print_index()

    elif cmd[0] == "SEARCH":
        print(len(db.exact_search(cmd[1], cmd[2])), "results found")

    elif cmd[0] == "RANGE":
        field = cmd[1]

        # Parse low and high, treating the string "None" as Python None
        low = None if len(cmd) <= 2 or cmd[2] == "None" else float(cmd[2])
        high = None if len(cmd) <= 3 or cmd[3] == "None" else float(cmd[3])

        # Call the BTree range search
        results = db.range_search(field, low, high)
        print(len(results), "results found")

    elif cmd[0] == "EXPORT":
        export_csv("Results.csv", db.last_results)
        print("Exported")

    elif cmd[0] == "DELETE":
        db.delete_results()
        print("Deleted")

    elif cmd[0] == "QUIT":
        break
    else:
        print("Control not found, make sure it is spelled correctly")