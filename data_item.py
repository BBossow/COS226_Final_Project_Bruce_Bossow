#This is the data item class to store all the different parts of the data from csv

class DataItem:
    def __init__(self, line):
        self.movie_name = line[0]
        self.genre = line[1]
        self.release_date = int(line[2])
        self.director = line[3]
        self.revenue = float(line[4])
        self.rating = float(line[5])
        self.min_duration = int(line[6])
        self.production_company = line[7]
        self.quote = line[8]