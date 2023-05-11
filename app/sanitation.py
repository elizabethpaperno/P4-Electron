import json
try:
    from db import query_usersdb
except:
    from db import query_usersdb

sanitation = open('app/datasets/sanitation.json')
data = json.load(sanitation)

violations = []
dba = []
grade = []
address = []

for res in data['data']:
    violations.append(str(res[14]))
    dba.append(str(res[9]))
    grade.append(str(res[17]))
    address.append(str(res[10]) + ' ' + str(res[11]) + ' ' + str(res[12]))

sanitation.close()

san_dict = {'vio': violations, 'dba': dba, 'grade': grade, 'address': address}

def get_sdict():
    return san_dict

def res_grade():
    res = query_usersdb("SELECT address FROM restuarants")

    i = 0
    while (i < res.len()):
        if(res[i] in san_dict[address][i]):
            query_usersdb(f"""UPDATE customers SET s_grade = ? WHERE address = ?;""", san_dict[grade][i], res[i])
