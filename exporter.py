import csv

def export_csv(filename, records):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "movie_name", "genre", "release_date", "director",
            "revenue", "rating", "min_duration",
            "production_company", "quote"
        ])
        for r in records:
            writer.writerow([
                r.movie_name, r.genre, r.release_date, r.director,
                r.revenue, r.rating, r.min_duration,
                r.production_company, r.quote
            ])