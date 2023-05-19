# Clyde 'Thluffy' Sinclair
# SoftDev
# Oct 2022

import sqlite3

from flask import Flask
from flask import render_template   
from flask import request          
from flask import session           
from flask import redirect, url_for 
from auth import *
from db import *
import os


app = Flask(__name__) #create instance of class Flask
app.secret_key = os.urandom(32)     #randomized string for SECRET KEY (for interacting with operating system)

@app.route('/main/<filters>')
def main(filters):
    return render_template('dashboard.html')

@app.route("/filter", methods = ["POST"])
def filter():
    #handle form
    if ("filter" in request.form):
        #get all the filters
        filters = request.form.getlist("filter")
        filters = "_".join(filters)
        #get data according to the filter
    return redirect("/main" + "/" + filters)
    


@app.route("/")       #assign fxn to route
def hello_world():
    print("the __name__ of this module is... ")
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
            return redirect("/main/dashboard")
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
        location = request.form['location']
        a_pref = request.form['alcohol_preference']
        s_pref = request.form['sanitation_preference']
        d_rest = request.form.getlist("diet_restrictions")
        d_rest = " ".join(d_rest)

        print(f_cat)

        updatePrefs(f_cat, location, a_pref, s_pref, d_rest, session["username"])
        return redirect("/main/dashboard")

    return render_template("survey.html")

#retrieves user preferences from database and returns a list of restaurant names and address that match aforementioned preferences
@app.route('/get_restaurants', methods = ["POST"])
def get_restaurants():
    obtain_restaurants(session["username"])

#retrieves a new review submitted and the address of the restaurant reviewed and adds the review to the review lists of both that user and restaurant in the database
@app.route('/add_review', methods = ["POST"])
def add_review():
    r_address = request.form['r_address']
    review = request.form['review']

    new_review(r_address, review, session["username"])

#retrieves address of restaurant to be added and adds it to the user's saved restaurants list in the database
@app.route('/add_restaurant', methods = ["POST"])
def add_restaurant():
    r_address = request.form['r_address']

    add_rest(r_address, session["username"])

#retrieves address of restaurant to be removed and removes it from the user's saved restaurants list in the database
@app.route('/remove_restaurant', methods = ["POST"])
def remove_restaurant():
    r_address = request.form['r_address']

    rem_rest(r_address, session["username"])

#retrieves address of restaurant to be added and adds it to the user's visited restaurants list in the database
@app.route('/add_visit', methods = ["POST"])
def add_visit():
    r_address = request.form['r_address']

    add_vis(r_address, session["username"])

#retrieves address of restaurant to be removed and removes it from the user's visited restaurants list in the database
@app.route('/remove_visit', methods = ["POST"])
def remove_visit():
    r_address = request.form['r_address']

    rem_vis(r_address, session["username"])

if __name__ == "__main__": # true if this file NOT imported
    createUsersTable() 
    print("users table created")
    app.debug = True        # enable auto-reload upon code change
    app.run()