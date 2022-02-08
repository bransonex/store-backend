"""
    Desc: Backend for the online store
Author: Kvon Smith

"""
from flask import Flask, abort, request, render_template
from mock_data import catalog
import json
from config import db, json_parse
from bson import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

about_me = {
    "name": "Kvon",
    "last": "Smith",
    "age": 29,
    "hobbies": [],
    "address": {
        "street":  "Windy Hill",
        "number" : "2377",
        "city": "Riverside"
    }
}



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


#*****************************************************
#********************API ENDPOINTS********************
#*****************************************************

@app.route("/api/catalog", methods=["get"])
def retrieve_catalog():
    # read data from the database (with no filter)
    cursor = db.products.find({})
    list = []
    for prod in cursor:
        print(prod)
        list.append(prod)

    return json_parse(list) # parse catalog into string and return it

@app.route("/api/catalog", methods=["post"])
def save_catalog():
    #get the payload (the objects/data that the client is sending)
    product = request.get_json()
    
    db.products.insert_one(product)
    return json_parse(product)

@app.route("/api/product/<id>")
def get_product(id):
    
    try:

        # id is a string, _id inside mongo is an ObjectId
        # we need to create an ObjectId instance fo the id string
        objectId_instance = ObjectId(id)
        # get a record by the id using PyMongo
        prod = db.products.find_one({"_id": objectId_instance}) # return an obj
        if prod is not None:
            return json_parse(prod)

        return abort(404) #return a 404 error (not found)
    
    except InvalidId:
        print("Error: Invalid Object ID", id)
        return abort(400) # return bad request

@app.route("/api/catalog/<category>")
def get_product_by_category(category):
    
    # pymongo get objects based on a property
    cursor = db.products.find({"category": category})
    # parse cursor into a list
    #return the list as a JSON string

    list = []
    for prod in cursor:
        print(prod)
        list.append(prod)

    return json_parse(list)

@app.route("/api/products/cheapest")
def get_cheapest_product():

    # migrate to DB
    # get all the prods from the DB
    cursor = db.products.find({})
    cheapest_prod = cursor[0]
    for prod in cursor:
        if (prod["price"] < cheapest_prod["price"]):
            cheapest_prod = prod
    return json_parse(cheapest_prod)
    
@app.route("/api/products/categories")
def get_unique_categories():
    cursor = db.products.find({})
    categories = []
    for prod in cursor:
        if prod["category"] not in categories:
            categories.append(prod["category"])

    return json_parse(categories)

@app.route("/api/reports/total")
def report_total():
    cursor = db.products.find({})
    total = 0
    for prod in cursor:
        total += prod["price"]

    return json_parse(total)
        
# /api/reports/total
# return the total ($ sum of prices) of the catalog





@app.route("/test/onetime/filldb")
def fill_db():
    for prod in catalog:
        # remove _id from the prod
        prod.pop("_id")

        # save the obj into the db
        db.products.insert_one(prod)

    return "Done!"


# TODO: remove debug before deploying
app.run(debug=True)