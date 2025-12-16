#This is the data item class to store all the different parts of the data from csv

class DataItem:
    def __init__(self, line):
        self.movie_name = line[0]
        self.genre = line[1]

        # Decided to go with just the year for this because of the formatting of it, so range queries are still possible
        self.release_date = int(line[2].split("/")[-1])

        self.director = line[3]

        # Same thing here with the formatting, simple fix is just to remove $
        self.revenue = float(line[4].replace("$", ""))
        
        self.rating = float(line[5])
        self.min_duration = int(line[6])
        self.production_company = line[7]
        self.quote = line[8]