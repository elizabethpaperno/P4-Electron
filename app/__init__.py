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

app = Flask(__name__) #create instance of class Flask

@app.route("/")       #assign fxn to route
def hello_world():
    print("the __name__ of this module is... ")
    print(__name__)
    return render_template("index.html")

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()

@app.route('/login_user', methods = ["POST"])
def login():
    if checkCreds(request.form['username'], request.form['password']):
        return redirect("main")
    

@app.route('/signup', methods = ["GET", "POST"])
def show_signup():
    print("hi")
    return render_template('signup.html')

@app.route('/create_user', methods = ["POST"])
def create_user():
    username = request.form['username']
    password = request.form['password']
    if checkUsernameAvailability(username):
        addNewUser(username, password)
    else:
        return render_template('signup.html', error = "Username already exists.")

@app.route('/main')
def main():
    return render_template('main.html')