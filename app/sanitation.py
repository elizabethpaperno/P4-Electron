import json

sanitation = open('app/datasets/sanitation.json')

data = json.load(sanitation)

#print(data['data'][0][17])

violations = []
dba = []
grade = []

for res in data['data']:
    violations.append(res[14])
    dba.append(res[9])
    grade.append(res[17])

print(violations)
sanitation.close()