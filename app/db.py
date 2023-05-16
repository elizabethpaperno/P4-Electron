import sqlite3
# from alcohol import *
# from sanitation import *

def get_connection(db):
    conn = sqlite3.connect(db)
    return conn


def query_db(query, args=(), all=False):
    conn = get_connection("P4.db")

    with conn:
        cur = conn.cursor()
        r = cur.execute(query, args)
        r = cur.fetchall()
    conn.close()

    return (r[0] if r else None) if not all else r

DB_FILE = "P4.db"
db_name = "P4.db"
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

#c.execute("""CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT, r_saved TEXT, r_visited TEXT, reviews TEXT, f_cat LIST, location TEXT, a_pref BOOL, s_pref TEXT, d_res LIST)""")
#c.execute("""CREATE TABLE IF NOT EXISTS retaurants(name TEXT, address TEXT, takeout BOOL, parking BOOL, cat LIST, hours DICT, reviews DICT, alcohol BOOL, mode TEXT, s_grade TEXT, vio TEXT, seating TEXT, diet LIST, u_reviews LIST)""")


