from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Flask Routes

@app.route("/")
def home():

    mars = mongo.db.collection.find_one()

    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = scrape_mars.scrape()

    mongo.db.collection.update({}, mars, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
