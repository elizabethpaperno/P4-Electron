import json

sanitation = open('app/datasets/sanitation.json')

data = json.load(sanitation)

print(data['data'][0])

violations = []
dba = []
grade = []
address = []

for res in data['data']:
    violations.append(str(res[14]))
    dba.append(str(res[9]))
    grade.append(str(res[17]))
    address.append(str(res[10]) + ' ' + str(res[11]) + ' ' + str(res[12]))

print(address)
sanitation.close()

def get_violations():
    return violations

def get_dba():
    return dba

def get_grade():
    return grade

# def get_address():
#     return address