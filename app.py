#################################################
# Import Dependencies
# @TODO: Import necessary libraries
#################################################

from flask import Flask, render_template
import scrape_mars  
from pymongo import MongoClient

#################################################
# Flask Setup
# @TODO: Initialize your Flask app here
#################################################
app = Flask(__name__)

#################################################
# MongoDB Setup
# @TODO: Initialize your MongoDB app here
#################################################

client = MongoClient("mongodb://localhost:27017")
db = client.mission_to_mars

#################################################
# MongoDB Mnipulation
# @TODO: Initialize your MongoDB app here
#################################################


#################################################
# Flask Routes
# @TODO:  Create a route and view function that takes in a string and renders index.html template
#################################################
@app.route("/")
def index():
    #use mars_info collection from mission_to_marsDB
    #query information from the collection and save to new_info
    new_info = db.mars_info.find_one()

    #if no database and collection yet (first-time), call scrape function and use
    #the scrape information to output object.
    if(new_info == None):
        output = scrape_mars.scrape()
        db.mars_info.insert_one(output)
        new_info = db.mars_info.find_one()

    for k, v in new_info.items(): 
        if k == "news":
            news = v
        elif k == "weather":                
            weather = v
        elif k == "featured_image_url":
            featured_image_url = v
        elif k == "facts":
            facts = v
        elif k == "hemisphere_image_urls": 
            hemisphere_image_urls = v

    return render_template('index.html',news=news,weather=weather,featured_image_url=featured_image_url,facts=facts,hemisphere_image_urls=hemisphere_image_urls)




        
# Route when the scrape button is click by user in the index.html
# Calls the scrape methods
# Remove the old mars_info collection in the mission_to_mars DB
# Insert th latest scrape information into the collection
# Render it into a dynamic html page        
@app.route("/scrape")
def scrape_new():
    output = scrape_mars.scrape()
    db.mars_info.remove({})
    db.mars_info.insert_one(output)
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)