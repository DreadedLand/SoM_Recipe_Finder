import sqlite3
import csv

con = sqlite3.connect("../recipes.db")
cursor = con.cursor()

cursor.execute("SELECT * FROM recipes")
rows = cursor.fetchall()

with open("../readable_recipe_db.csv", "w", newline='', encoding="UTF-8") as file:
    writer = csv.writer(file)

    writer.writerow([description[0] for description in cursor.description])
    # ^^ this basically gets the first row (column) of each description
    writer.writerows(rows)  # this writes the rest of the rows

con.close()