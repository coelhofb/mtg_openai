#Import Dependencies
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, render_template, request, url_for
from datetime import date, datetime, timezone
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from magic_open_ai import *


#App Constants
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_PATH = os.getenv("MONGO_PATH")
MONGO_CONN = 'mongodb://'+ MONGO_USER +':' + MONGO_PASS + '@'+os.getenv("MONGO_PATH")

OUT_IMG_PATH = 'static/cards/'
DB_MTG_CARDS = 'db_mtg_cards'
DB_MTG_CARDS_COLLECTION = 'db_mtg_cards_collection'

app = Flask(__name__)

#Initial Blank Page
@app.route("/", methods=("GET", "POST"))
def index():    
    return render_template("index.html",blank=True)

#Generate New Card
@app.route("/generate", methods=("GET", "POST"))    
def generate_card():
    received_post = request.form.to_dict()
    theme = received_post["theme"]
        
    mtg_card = {}
    mtg_card_img = ''
    
    try:
        mtg_card = generate_mtg_card(theme)
        #try:
        #      mtg_card_img = generate_illustration(mtg_card["theme"], mtg_card["name"],mtg_card["type"],OUT_IMG_PATH)
        #except:
        #      mtg_card_img = 'error.png'

        mtg_card["date"] = datetime.now(tz=timezone.utc)
        mtg_card["illustration"] = mtg_card_img
       
        #Store in Mongo DB
        card_id = ''
        with MongoClient(MONGO_CONN) as client:
            db = client[DB_MTG_CARDS]
            collection = db[DB_MTG_CARDS_COLLECTION]
            card_id = str(collection.insert_one(mtg_card).inserted_id)

        return redirect("/"+card_id)
        
    except Exception as e:
        mtg_card = {"name": 'Error generating Mtg Card'}
        print(str(e))
        return render_template("index.html", mtg_card=mtg_card , out_img_path=OUT_IMG_PATH)
    
#Load Last Generated Card
@app.route("/load", methods=("GET", "POST"))    
def load_card():
    mtg_card = {}
    with MongoClient(MONGO_CONN) as client:
        db = client[DB_MTG_CARDS]
        collection = db[DB_MTG_CARDS_COLLECTION] 
        mtg_card = collection.find_one(sort=[( 'date', DESCENDING )])
        client.close()
        return redirect("/"+str(mtg_card["_id"]))
  
    r#eturn render_template("index.html", mtg_card=mtg_card, out_img_path=OUT_IMG_PATH)

#Load Specific Card Id
@app.route("/<card_id>", methods=("GET", "POST"))    
def load_card_id(card_id):
    mtg_card = {}
    with MongoClient(MONGO_CONN) as client:
        db = client[DB_MTG_CARDS]
        collection = db[DB_MTG_CARDS_COLLECTION]
        mtg_card = collection.find({"_id": ObjectId(card_id)})[0]
        client.close()
       
        mtg_card["ability"] = adjust_ability(mtg_card["ability"])
  
    return render_template("index.html", mtg_card=mtg_card, out_img_path=OUT_IMG_PATH)

#Load Random Card
@app.route("/load_random_card", methods=("GET", "POST"))    
def load_random_card():
    mtg_card = {}
    with MongoClient(MONGO_CONN) as client:
        db = client[DB_MTG_CARDS]
        collection = db[DB_MTG_CARDS_COLLECTION]
        sample = collection.aggregate([{ "$sample": { "size": 1 } }])
        mtg_card = list(sample)[0]
        client.close()

        mtg_card["ability"] = adjust_ability(mtg_card["ability"])
  
    return render_template("index.html", mtg_card=mtg_card , out_img_path=OUT_IMG_PATH)
