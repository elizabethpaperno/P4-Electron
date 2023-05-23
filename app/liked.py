import sqlite3
try:
    from db import query_db
except:
    from db import query_db

def createLikedRestTable():
    # conn = sqlite3.connect("P4.db")
    # cur = conn.cursor()
    #query_db("DROP TABLE IF EXISTS liked_rest;")
    query_db("CREATE TABLE IF NOT EXISTS liked_rest(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, rest_name TEXT);")
    # conn.close()
    
def addRestaurant(user,rest_name):
    # conn = sqlite3.connect("P4.db")
    # cur = conn.cursor()
    query_db("INSERT INTO liked_rest (username, rest_name) VALUES (?,?);", (user, rest_name))
    #conn.close()
    
def getListLikedRestaurants(user):
    conn = sqlite3.connect("P4.db")
    cur = conn.cursor()
    unformatted = cur.execute('SELECT rest_name FROM liked_rest WHERE username = ?;', (user, )).fetchall()
    #unformatted = query_db('SELECT rest_name FROM liked_rest WHERE username = ?;', (user, ))
    conn.close()
    formatted = []
    for i in unformatted:
        formatted.append(i[0])
    return formatted

if __name__ == "__main__":
    createLikedRestTable()
    #addRestaurant("epap", "filler1")
    #addRestaurant("epap", "filler2")
    #addRestaurant("rty","wassup")
    print(getListLikedRestaurants("rty"))
