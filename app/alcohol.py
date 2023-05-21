import json
try:
    from db import query_db
except:
    from db import query_db

#open JSON as Python dict
alcohol = open('app/datasets/alcohol.json')
data = json.load(alcohol) 

#initiate lists to fill with data from dataset
p_name = []
mode = []
address = []

#loops through each restuarant in the data and records its desired data
for res in data['data']:
    p_name.append(res[13])
    mode.append(res[22])
    address.append(str(res[15]))

alcohol.close()

#create dict containing on desired data retrived from dataset
alc_dict = {'name': p_name, 'mode': mode, 'address': address}

def get_adict():
    return alc_dict

#checks if each restaurant in database is liscensed to sell alcohol
def alcohol_yn():
    res = query_db("SELECT address FROM restaurants")
    # print(res)

    i = 0
    while (i < len(res)):
        if(res[i] in alc_dict['address'][i]):
            query_db(f"""UPDATE restaurants SET alcohol = ? WHERE address = ?;""", (True, res[i]))
            query_db(f"""UPDATE restaurants SET mode = ? WHERE address = ?;""", (alc_dict['mode'][i], res[i]))
        else:
            query_db(f"""UPDATE restaurants SET alcohol = ? WHERE address = ?;""", (False, res[i]))

def getAlc(address):
    return query_db(f"""SELECT alcohol FROM restaurants WHERE address = ?;""", (address))

# alcohol_yn()
# print(alc_dict['address'][0])
# print(getAlc("1356 W SWEDEN RD"))
    