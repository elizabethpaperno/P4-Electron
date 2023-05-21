# Electron
# SoftDev
# May 2023

import sqlite3

from flask import Flask
from flask import render_template   
from flask import request          
from flask import session           
from flask import redirect, url_for 
from auth import *
from db import *
import os
import yelp
import pandas as pd


app = Flask(__name__) #create instance of class Flask
app.secret_key = os.urandom(32)     #randomized string for SECRET KEY (for interacting with operating system)

@app.route('/main', methods = ['GET', 'POST'])
def main():
    addresses = []
    if request.method == "POST":
        if ("filter" in request.form):
            #get all the filters
            filters = request.form.getlist("filter")
            #print("_".join(filters))
            #print(filters)
            #get data according to the filter
            addresses = yelp.getFilteredListAddresses(df,filters=filters)
            #print(addresses[0])
            #convert to a string that's easier to work with in JS
            addresses = ";".join(addresses)

    # data = request.form["Halal"]
    # print(data)
    return render_template('dashboard.html', addresses = addresses)

@app.route("/")       #assign fxn to route
def hello_world():
    print(list(df.columns.values))
    print("the __name__ of this module is... ")
    print(list(df.columns.values))
    print(__name__)
    return render_template("index.html")

@app.route('/login_user', methods = ["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    if checkCreds(username, password):
        session["username"] = username

        if not checkPrefs(username):
            return redirect("/survey")
        else:
            return redirect(url_for('main'))
    else: 
        return render_template('index.html', error = "Incorrect username or password")
    #needs a return statement here otherwise the app fails if credentials are not valid

@app.route('/create_user', methods = ["POST"])
def create_user():
    username = request.form['username']
    password = request.form['password']
    if checkUsernameAvailability(username):
        addNewUser(username, password)
        return render_template('index.html', error = "Account successfully created.")
    else:
        return render_template('signup.html', error = "Username already exists.")

@app.route('/signup', methods = ["GET", "POST"])
def show_signup():
    print("hi")
    return render_template('signup.html')

#retrieves user preferences from survey and updates them in the database
@app.route('/survey', methods = ["GET", "POST"])
def survey():
    questionsAsked = ['food_category', 'location', 'alcohol_preference', 'sanitation_preference', 'diet_restrictions']
    if (request.method == "POST") and not checkPrefs(session['username']):
        print(request.form)
        for question in questionsAsked:
            if question not in request.form:
                print("no answer given for " + question)
                return render_template("survey.html", error = "please fill out the entire form")
            if request.form['location'].strip() == "":
                return render_template("survey.html", error = "please fill out the entire form")
            
        f_cat = request.form.getlist("food_category")
        f_cat = " ".join(f_cat)

        f_cat = request.form['food_category']
        location = request.form['location']
        a_pref = request.form['alcohol_preference']
        s_pref = request.form['sanitation_preference']
        d_rest = request.form.getlist("diet_restrictions")
        d_rest = " ".join(d_rest)

        updatePrefs(f_cat, location, a_pref, s_pref, d_rest, session["username"])
        return redirect("/main")

    return render_template("survey.html")

# @app.route('/get_restaurants', methods = ["POST"])
# def get_restaurants():
#     name_address = query_usersdb(f"""SELECT name, address FROM restaurants WHERE cat = ?, alcohol = ?, diet != ?;""", )

#retrieves user preferences from database and returns a list of restaurant names and address that match aforementioned preferences
@app.route('/get_restaurants', methods = ["POST"])
def get_restaurants():
    f_cat = query_db(f"""SELECT f_cat FROM users WHERE username = ?;""", session["username"])
    a_pref = query_db(f"""SELECT a_pref FROM users WHERE username = ?;""", session["username"])
    s_pref = query_db(f"""SELECT s_pref FROM users WHERE username = ?;""", session["username"])
    d_res = query_db(f"""SELECT d_res FROM users WHERE username = ?;""", session["username"])

    name_address = query_db(f"""SELECT name, address FROM restaurants WHERE cat = ?, alcohol = ?, seating = ?, diet != ?;""", f_cat, a_pref, s_pref, d_res)
    return name_address

#retrieves a new review submitted and the address of the restaurant reviewed and adds the review to the review lists of both that user and restaurant in the database
@app.route('/add_review', methods = ["POST"])
def add_review():
    r_address = request.form['r_address']
    review = request.form['review']

    current_rreviews = query_db(f"""SELECT u_reviews FROM restaurants WHERE address = ?""", r_address)
    new_rreviews = current_rreviews.append(review)
    query_db(f"""UPDATE restaurants SET u_reviews = ? WHERE address = ?;""", new_rreviews, r_address)

    current_ureviews =  query_db(f"""SELECT reviews FROM users WHERE username = ?;""", session["username"])
    new_ureviews = current_ureviews.append(review)
    query_db(f"""UPDATE users SET reviews = ? WHERE username = ?""", new_ureviews, session["username"])

#retrieves address of restaurant to be added and adds it to the user's saved restaurants list in the database
@app.route('/add_restaurant', methods = ["POST"])
def add_restaurant():
    r_address = request.form['r_address']

    current_list = query_db(f"""SELECT r_saved FROM users WHERE username = ?;""", session["username"])
    new_list = current_list.append(r_address)
    query_db(f"""UPDATE users SET r_saved = ? WHERE username = ?;""", new_list, session["username"])

#retrieves address of restaurant to be removed and removes it from the user's saved restaurants list in the database
@app.route('/remove_restaurant', methods = ["POST"])
def remove_restaurant():
    r_address = request.form['r_address']

    current_list = query_db(f"""SELECT r_saved FROM users WHERE username = ?;""", session["username"])
    new_list = current_list.pop(r_address)
    query_db(f"""UPDATE users SET r_saved = ? WHERE username = ?;""", new_list, session["username"])

#retrieves address of restaurant to be added and adds it to the user's visited restaurants list in the database
@app.route('/add_visit', methods = ["POST"])
def add_visit():
    r_address = request.form['r_address']

    current_list = query_db(f"""SELECT r_visited FROM users WHERE username = ?;""", session["username"])
    new_list = current_list.append(r_address)
    query_db(f"""UPDATE users SET r_visited = ? WHERE username = ?;""", new_list, session["username"])

#retrieves address of restaurant to be removed and removes it from the user's visited restaurants list in the database
@app.route('/remove_visit', methods = ["POST"])
def remove_visit():
    r_address = request.form['r_address']

    current_list = query_db(f"""SELECT r_visited FROM users WHERE username = ?;""", session["username"])
    new_list = current_list.pop(r_address)
    query_db(f"""UPDATE users SET r_visited = ? WHERE username = ?;""", new_list, session["username"])

if __name__ == "__main__": # true if this file NOT imported
    createUsersTable() 
    print("users table created")
    df = pd.read_json("yelp.json")
    df = yelp.editDF(df)
    app.debug = True        # enable auto-reload upon code change
    app.run()