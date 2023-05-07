try:
    from db import query_usersdb
except:
    from db import query_usersdb

#add other cols later
def createUsersTable(): 
    query_usersdb("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")

def addNewUser(username, password): 
    query_usersdb("INSERT INTO users VALUES (?, ?);", (username, password))

def checkUsernameAvailability(username):
    user = query_usersdb("SELECT * FROM users WHERE username = ?", (username,))
    return user is None

def checkCreds(username, password):
    user = query_usersdb("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return user is not None

def update_user_password(username, password):
    query_usersdb("UPDATE users SET password = ? WHERE username = ?", (username, password))

def delete_user(username):
    query_usersdb("DELETE FROM users WHERE username = ?", (username))

def get_user_password(username):
    password = query_usersdb("SELECT password FROM users WHERE username = ?", (username,))
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