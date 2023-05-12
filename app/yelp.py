import json
import sqlite3
import db
import pandas as pd
#try:
    #from db import query_db
#except:
    #from db import query_db

def createYelpTable(): 
    with open("app/yelp_academic_dataset_business.json", "r") as f:
        df = pd.read_json(f, lines=True)
    df.to_json("app/business.json")
    business_json = json.load(open("app/business.json"))
    #print(business_json)

    db.query_db("CREATE TABLE IF NOT EXISTS yelp (business_id TEXT, name TEXT PRIMARY KEY, address TEXT, city TEXT, state TEXT, postal_code TEXT, latitude REAL, longitude REAL, stars REAL, review_count INT, is_open INT, attributes BLOB, categories BLOB, hours BLOB)")

    db.query_db("INSERT INTO yelp SELECT json_extract(value, '$.business_id'), json_extract(value, '$.name'), json_extract(value, '$.address'), json_extract(value, '$.city'), json_extract(value, '$.state'), json_extract(value, '$.postal code'),json_extract(value, '$.latitude'),json_extract(value, '$.longitude'),json_extract(value, '$.stars'),json_extract(value, '$.review_count'),json_extract(value, '$.is_open'),json_extract(value, '$.attributes'),json_extract(value, '$.categories'),json_extract(value, '$.hours') FROM json_each(?);",(business_json,))
    '''
    columns = [] 
    column = [] 

    for data in business_json: 
        print(data)
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

    
    db.query_db("INSERT INTO yelp values (?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?, ?, ?)")
    '''

# LINES BELOW ONLY GET RUN IF "EXPLICITY RAN" with `python3 app/yelp.py`
if __name__ == "__main__":
    createYelpTable()
    #query_db("SELECT * FROM yelp")
    #print(cur.fetchall())