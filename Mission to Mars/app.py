from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    marspage = mongo.db.marspages.find_one()
    return render_template("index.html", marspage=marspage)

@app.route("/scrape")
def scraper():
    marspage = mongo.db.marspages
    marspagedata = scrape_mars.scrape()
    marspage.update({}, marspagedata, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)