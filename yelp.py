import json
import sqlite3
import db
import pandas as pd
#try:
    #from db import query_db
#except:
    #from db import query_db

def createYelpTable(): 
    df = pd.read_json('app/yelp_academic_dataset_business.json', lines=True)
    df.to_json("app/business.json")
    business_json = json.load(open("app/business.json"))
    
    columns = [] 
    column = [] 
    for data in business_json: 
        column = list(data.keys())
        for col in column: 
            if col not in columns: 
                columns. apppend(col)

    value = [] 
    values = [] 

    for data in business_json: 
        for i in columns: 
            value.append(str(dict(data)))
        values.append(list(value))
        value.clear()

    db.query_db("CREATE TABLE IF NOT EXISTS yelp (business_id, name, address, city, state, postal code, latitude, longitude, stars, review_count, is_open, attributes, categories, hours)")
    db.query_db("INSERT INTO yelp values (?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?, ?, ?)")


# LINES BELOW ONLY GET RUN IF "EXPLICITY RAN" with `python3 app/yelp.py`
if __name__ == "__main__":
    createYelpTable()
    #query_db("SELECT * FROM yelp")
    #print(cur.fetchall())