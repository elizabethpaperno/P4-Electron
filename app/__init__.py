# Clyde 'Thluffy' Sinclair
# SoftDev
# Oct 2022

import sqlite3
from flask import Flask
from flask import render_template   
from flask import request          
from flask import session           
from flask import redirect, url_for 

app = Flask(__name__) #create instance of class Flask

@app.route("/")       #assign fxn to route
def hello_world():
    print("the __name__ of this module is... ")
    print(__name__)
    return render_template("login.html")

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()
