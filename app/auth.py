try:
    from db import query_db
except:
    from db import query_db
import db
#add other cols later
def createUsersTable(): 
    #db.query_db("DROP TABLE IF EXISTS users;")
    query_db("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)")
    query_db("CREATE TABLE IF NOT EXISTS preferences(f_cat TEXT, location TEXT, a_pref TEXT, s_pref INTEGER, username TEXT PRIMARY KEY)")

def addNewUser(username, password): 
    db.query_db("INSERT INTO users VALUES (?, ?);", (username, password))

def checkUsernameAvailability(username):
    user = db.query_db("SELECT * FROM users WHERE username = ?", (username,))
    return user is None

def checkCreds(username, password):
    user = db.query_db("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return user is not None

def updateUserPassword(username, password):
    db.query_db("UPDATE users SET password = ? WHERE username = ?", (username, password))

def deleteUser(username):
    db.query_db("DELETE FROM users WHERE username = ?", (username))

def getUserPassword(username):
    password = db.query_db("SELECT password FROM users WHERE username = ?", (username,))
    return password

def updatePrefs(f_cat, location, a_pref, s_pref, username):
    query_db("REPLACE INTO preferences VALUES (?, ?, ?, ?, ?)", (f_cat, location, a_pref, s_pref, username))

def checkPrefs(username):
    prefs = db.query_db("SELECT * FROM preferences WHERE username = ?", (username,))
    return prefs is not None

# LINES BELOW ONLY GET RUN IF "EXPLICITY RAN" with `python app/auth.py`
if __name__ == "__main__":
    create_user_info_table()
    print(check_username_availability("epap"))
    add_new_user("epap", "hi", "123")
    print(check_creds("epap", "hi"))
    print(check_creds("epap", "hi2"))
    print(check_username_availability("epap"))