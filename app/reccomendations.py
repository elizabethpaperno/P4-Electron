import auth
import yelp
import db
import match
import pandas as pd

#returns list formatted like [[rest_add1, score1], [rest_add2, score2]]
def getListScoreAddresses(df, sa_data, username):
    list = []
    # hardcoded for now
    cuisine_multiplier = 40
    location_multiplier = 40
    alcohol_multiplier = 25
    dietary_multiplier = 50
    f_cat = db.query_db(f"""SELECT f_cat FROM preferences WHERE username = ?;""", (username,))[0].split(",")
    location = db.query_db(f"""SELECT location FROM preferences WHERE username = ?;""", (username,))[0].split(",")
    a_pref = bool(db.query_db(f"""SELECT a_pref FROM preferences WHERE username = ?;""", (username,))[0])
    s_pref = int(db.query_db(f"""SELECT s_pref FROM preferences WHERE username = ?;""", (username,))[0])
    d_rest = db.query_db(f"""SELECT d_rest FROM preferences WHERE username = ?;""", (username,))[0].split(",")
    addresses = yelp.getListAllAddresses(df)
    for address in addresses:
        score = 0
        cats = yelp.getFormattedCategories(df, address).split(",")
        common_cats = [c for c in cats if c in f_cat]
        score += len(common_cats) * cuisine_multiplier
        common_dietary = [c for c in cats if c in d_rest]
        score += len(common_dietary) * dietary_multiplier
        if (a_pref == bool(match.getAlcohol(yelp.getShortAddress(df,address))):
            score += alcohol_multiplier
        if (sa_data[yelp.getShortAddress(df,address)]["score"] >= s_pref):
            score += sa_data[yelp.getShortAddress(df,address)]["score"]
        neighborhood = yelp.getNeighborhood(df, address)
        if neighborhood in location:
            score += location_multiplier
        if (score >= 100):
            list.append([address, score])
    return list

if __name__ == "__main__":
    df = pd.read_json("yelp.json")
    df = yelp.editDF(df)
    print(getListScoreAddresses(df, sa_data, "epap5"))
