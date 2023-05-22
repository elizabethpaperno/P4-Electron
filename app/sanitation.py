import json
try:
    from db import query_db
except:
    from db import query_db

from difflib import SequenceMatcher

#open JSON as Python dict
sanitation = open('app/datasets/sanitation.json')
data = json.load(sanitation)

#initiate lists to fill with data from dataset
violations = []
dba = []
#grade = []
score = []
address = []

#loops through each restuarant in the data and records its desired data
for res in data['data']:
    if (res[9] == "Manhattan"):
        violations.append(str(res[14]))
        dba.append(str(res[9]))
        #grade.append(str(res[17]))
        score.append(int(res[16]))
        address.append(str(res[10]) + ' ' + str(res[11]))

sanitation.close()

#create dict containing on desired data retrived from dataset
san_dict = {'vio': violations, 'dba': dba, 'score': score, 'address': address}

def get_sdict():
    return san_dict

def res_grade():
    res = query_db("SELECT address FROM restaurants")

    i = 0
    while (i < len(res)):
        if(res[i] in san_dict['address'][i]):
            query_db(f"""UPDATE restaurants SET s_grade = ? WHERE address = ?;""", (san_dict['grade'][i], res[i]))

def res_vio():
    res = query_db("SELECT address FROM restaurants")

    i = 0
    while (i < res.len()):
        query_db(f"""UPDATE restaurants SET vio = ? WHERE address = ?;""", (san_dict['vio'][i], res[i]))

def getGrade(address):
    return query_db(f"""SELECT s_grade FROM restaurants WHERE address = ?;""", (address))

def getVio(address):
    return query_db(f"""SELECT vio FROM restaurants WHERE address = ?;""", (address))