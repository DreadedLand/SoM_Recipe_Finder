# import data into website and make search work

from flask import request, Flask, render_template
import sqlite3

app = Flask(__name__)

def get_recipes(query=""):  # default is ""
    con = sqlite3.connect("recipes.db")
    curs = con.cursor()

    if query:
        curs.execute("SELECT * FROM recipes WHERE title LIKE ? OR ingredients LIKE ?", (f"%{query}%",f"%{query}%"))
    else:
        curs.execute("SELECT * FROM recipes")
    recipes = curs.fetchall()
    con.close()
    return recipes

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("search", "")
    recipes = get_recipes(query)
    return render_template("index.html", recipes=recipes, query=query)

if __name__ == "__main__":
    app.run(debug=True)  # debug data on startup