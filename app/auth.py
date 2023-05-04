try:
    from db import query_db
except:
    from db import query_db

#add other cols later
def createUsersTable(): 
    query_db("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT")

def addNewUser(username, password): 
    query_db("INSERT INTO users VALUES (?, ?);", (username, password))

def checkUsernameAvailability(username):
    user = query_db("SELECT * FROM users WHERE username = ?", (username,))
    return user is None

def checkCreds(username, password):
    user = query_db("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return user is not None

def update_user_password(username, password):
    query_db("UPDATE users SET password = ? WHERE username = ?", (username, password))

def delete_user(username):
    query_db("DELETE FROM users WHERE username = ?", (username))

def get_user_password(username):
    password = query_db("SELECT password FROM users WHERE username = ?", (username,))
    return password
    
# LINES BELOW ONLY GET RUN IF "EXPLICITY RAN" with `python app/db/auth.py`
if __name__ == "__main__":
    create_user_info_table()
    print(check_username_availability("epap"))
    add_new_user("epap", "hi", "123")
    print(check_creds("epap", "hi"))
    print(check_creds("epap", "hi2"))
    print(check_username_availability("epap"))
    # print(get_zipcoe("epap"))