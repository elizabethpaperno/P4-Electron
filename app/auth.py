try:
    from db import query_db
except:
    from db import query_db
import db
#add other cols later
def createUsersTable(): 
    #db.query_db("DROP TABLE IF EXISTS users;")
    query_db("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)")
    query_db("CREATE TABLE IF NOT EXISTS preferences(f_cat TEXT, location TEXT, a_pref TEXT, s_pref INTEGER, d_rest TEXT, username TEXT PRIMARY KEY)")

def createRestaurantTable():
    query_db("CREATE TABLE IF NOT EXISTS restaurants(name TEXT, address TEXT, alcohol BOOL, sanitation INT)")

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

def updatePrefs(f_cat, location, a_pref, s_pref, d_rest, username):
    query_db("REPLACE INTO preferences VALUES (?, ?, ?, ?, ?, ?)", (f_cat, location, a_pref, s_pref, d_rest, username,))

def checkPrefs(username):
    prefs = db.query_db("SELECT * FROM preferences WHERE username = ?", (username,))
    return prefs is not None

def obtain_restaurants(username):
    f_cat = query_db(f"""SELECT f_cat FROM preferences WHERE username = ?;""", (username,))
    location = query_db(f"""SELECT location FROM preferences WHERE username = ?;""", (username,))
    a_pref = query_db(f"""SELECT a_pref FROM preferences WHERE username = ?;""", (username,))
    s_pref = query_db(f"""SELECT s_pref FROM preferences WHERE username = ?;""", (username,))
    d_rest = query_db(f"""SELECT d_rest FROM preferences WHERE username = ?;""", (username,))

    name_address = query_db(f"""SELECT name, address FROM restaurants WHERE cat = ?, loc = ?, alcohol = ?, seating = ?, diet != ?;""", (f_cat, location, a_pref, s_pref, d_rest,))
    return name_address

def new_review(r_address, review, username):
    current_rreviews = query_db(f"""SELECT u_reviews FROM restaurants WHERE address = ?""", (r_address,))
    new_rreviews = current_rreviews.append(review)
    query_db(f"""UPDATE restaurants SET u_reviews = ? WHERE address = ?;""", (new_rreviews, r_address,))

    current_ureviews =  query_db(f"""SELECT reviews FROM users WHERE username = ?;""", (username,))
    new_ureviews = current_ureviews.append(review)
    query_db(f"""UPDATE users SET reviews = ? WHERE username = ?""", (new_ureviews, username,))

def add_rest(r_address, username):
    current_list = query_db(f"""SELECT r_saved FROM users WHERE username = ?;""", (username,))
    new_list = current_list.append(r_address)

    query_db(f"""UPDATE users SET r_saved = ? WHERE username = ?;""", (new_list, username,))

def rem_rest(r_address, username):
    current_list = query_db(f"""SELECT r_saved FROM users WHERE username = ?;""", (username,))
    new_list = current_list.pop(r_address)

    query_db(f"""UPDATE users SET r_saved = ? WHERE username = ?;""", (new_list, username,))

def add_vis(r_address, username):
    current_list = query_db(f"""SELECT r_visited FROM users WHERE username = ?;""", (username,))
    new_list = current_list.append(r_address)

    query_db(f"""UPDATE users SET r_visited = ? WHERE username = ?;""", (new_list, username,))

def rem_vis(r_address, username):
    current_list = query_db(f"""SELECT r_visited FROM users WHERE username = ?;""", (username,))
    new_list = current_list.pop(r_address)

    query_db(f"""UPDATE users SET r_visited = ? WHERE username = ?;""", (new_list, username,))

# LINES BELOW ONLY GET RUN IF "EXPLICITY RAN" with `python app/auth.py`
if __name__ == "__main__":
    create_user_info_table()
    print(check_username_availability("epap"))
    add_new_user("epap", "hi", "123")
    print(check_creds("epap", "hi"))
    print(check_creds("epap", "hi2"))
    print(check_username_availability("epap"))