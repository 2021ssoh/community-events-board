import os
from app import app
from flask import render_template, request, redirect

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"}
    ]


from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'database-name'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:SUdKE0PRiU1r4Ihv@cluster0-f3oyp.mongodb.net/test?retryWrites=true&w=majority'

# mongo is an instance of the PyMongo class
mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    # connect to the MONGO_DB
    collection = mongo.db.events
    # find all events in database using a query
    # {} will return everything in the database
    events = list(collection.find({}))
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    collection = mongo.db.events
    # insert new data
    collection.insert({"event_name": "test", "event_date": "today"})
    # return a message to the user
    return "you added an event to the database! go check it!!"

# need a get and a post method
@app.route('/results', methods = ["get", "post"])
def results():
    # store userinfo from the form
    user_info = dict(request.form)
    print(user_info)
    #store the event_name
    event_name = user_info["event_name"]
    print("the event name is ", event_name)
    #store the event_date
    event_date = user_info["event_date"]
    print("the event date is ", event_date)
    # store category
    category = user_info["category"]
    print("the category is ", category)
    # store price
    cost = user_info["cost"]
    print("the price is ", cost)
    #connect to Mongo DB
    collection = mongo.db.events
    #insert the user's input event_name and event_date to MONGO, add category in database
    collection.insert({"event_name": event_name, "event_date": event_date, "category": category, "cost": cost})
    #(so that it will continue to exist after this program stops)
    events = list(collection.find({}))
    return render_template('index.html', events = events)


@app.route('/delete_all')
def delete_all():
    # connect to MONGO_DB
    # collection - is storing the data in mongo
    collection = mongo.db.events
    # delete everything
    # google search terms pymongo delete many objects from database
    # the {} find all objects in the database to delete them
    collection.delete_many({})
    # redirect back to index page**
    return redirect('/index')

@app.route('/input_event')
def input_event():
    return render_template('event.html')

@app.route('/diff_category')
def diff_category():
    return render_template('category.html')


@app.route('/filter', methods = ["get", "post"])
def filter():
    user_info = dict(request.form)
    print(user_info)
    collection = mongo.db.events
    category = user_info["category"]
    print(category)
    school_events = list(collection.find({"category": category}))
    print(school_events)
    return render_template('filter.html', events = school_events, category = category)
