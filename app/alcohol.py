import json
try:
    from db import query_usersdb
except:
    from db import query_usersdb

alcohol = open('app/datasets/alcohol.json')
data = json.load(alcohol)

p_name = []
mode = []
address = []

for res in data['data']:
    p_name.append(res[13])
    mode.append(res[22])
    address.append(str(res[15]) + ' ' + str(res[19]))

alcohol.close()

alc_dict = {'name': p_name, 'mode': mode, 'address': address}

def get_adict():
    return alc_dict

def alcohol_yn():
    res = query_usersdb("SELECT address FROM restuarants")
    alc = alc_dict['address']

    #print(alc)

    for r in res:
        if(r in alc):
            query_usersdb("""UPDATE customers SET alcohol = ? WHERE address = ?""", True, r)
        else:
            query_usersdb("""UPDATE customers SET alcohol = ? WHERE address = ?""", True, r)