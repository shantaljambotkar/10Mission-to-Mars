from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"  #Uniform resource identifier
mongo = PyMongo(app) 

#Define the route for the HTML page
@app.route("/")  #homepage
def index():
   mars = mongo.db.mars.find_one()  # PyMongo to find the "mars" collection in our database
   print(mars)
   return render_template("index.html", mars=mars) #tells Flask to return an HTML template using an index.html file and tells Python to use the "mars" collection in MongoDB

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   print(mars_data)
   mars.update({}, mars_data, upsert=True) #Upsert indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved
   return redirect('/', code=302)

#save the work
if __name__ == "__main__":
   app.run()