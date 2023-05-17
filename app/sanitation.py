import json
try:
    from db import query_db
except:
    from db import query_db

#open JSON as Python dict
sanitation = open('app/datasets/sanitation.json')
data = json.load(sanitation)

#initiate lists to fill with data from dataset
violations = []
dba = []
grade = []
address = []

#loops through each restuarant in the data and records its desired data
for res in data['data']:
    violations.append(str(res[14]))
    dba.append(str(res[9]))
    grade.append(str(res[17]))
    address.append(str(res[10]) + ' ' + str(res[11]) + ' ' + str(res[12]))

sanitation.close()

#create dict containing on desired data retrived from dataset
san_dict = {'vio': violations, 'dba': dba, 'grade': grade, 'address': address}

def get_sdict():
    return san_dict

def res_grade():
    res = query_db("SELECT address FROM restuarants")

    i = 0
    while (i < res.len()):
        if(res[i] in san_dict['address'][i]):
            query_db(f"""UPDATE restuarants SET s_grade = ? WHERE address = ?;""", san_dict['grade'][i], res[i])

def res_vio():
    res = query_db("SELECT address FROM restuarants")

    i = 0
    while (i < res.len()):
        query_db(f"""UPDATE restuarants SET vio = ? WHERE address = ?;""", san_dict['vio'][i], res[i])