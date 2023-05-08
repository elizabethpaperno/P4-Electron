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

@app.route('/main')
def main():
    return render_template('main.html')

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

if __name__ == "__main__": # true if this file NOT imported
    createUsersTable() 
    app.debug = True        # enable auto-reload upon code change
    app.run()