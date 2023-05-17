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
try:
    from db import query_usersdb
except:
    from db import query_usersdb
import os


app = Flask(__name__) #create instance of class Flask
app.secret_key = os.urandom(32)     #randomized string for SECRET KEY (for interacting with operating system)

@app.route('/main')
def main():
    return render_template('dashboard.html')

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
        session["username"]= username
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
        return render_template('signup.html', error = "Successfully created account")
    else:
        return render_template('signup.html', error = "Username already exists.")

@app.route('/signup', methods = ["GET", "POST"])
def show_signup():
    print("hi")
    return render_template('signup.html')

@app.route('/survey', methods = ["GET", "POST"])
def survey():
    if (request.method == "POST")
        f_cat = request.form['f_cat']
        location = request.form['location']
        a_pref = request.form['a_pref']
        s_pref = request.form['s_pref']
        d_res = request.form['d_res']
        query_usersdb(f"""UPDATE users SET f_cat = ?, location = ?, a_pref = ?, s_pref = ?, d_res = ? WHERE username = ?;""", f_cat, location, a_pref, s_pref, d_res, session["username"])
    return render_template("survey.html")

# @app.route('/get_restaurants', methods = ["POST"])
# def get_restaurants():
#     name_address = query_usersdb(f"""SELECT name, address FROM restaurants WHERE cat = ?, alcohol = ?, diet != ?;""", )

@app.route('/add_review', methods = ["POST"])
def add_review():
    r_address = request.form['r_address']
    review = request.form['review']
    current_reviews = query_usersdb(f"""SELECT u_reviews FROM restaurants WHERE address = ?""", r_address)
    new_reviews = current_reviews.append(review)

    query_usersdb(f"""UPDATE restaurants SET u_reviews = ? WHERE address = ?;""", new_reviews, r_address)

if __name__ == "__main__": # true if this file NOT imported
    createUsersTable() 
    app.debug = True        # enable auto-reload upon code change
    app.run()