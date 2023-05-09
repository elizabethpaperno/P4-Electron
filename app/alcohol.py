import json

alcohol = open('app/datasets/alcohol.json')

data = json.load(alcohol)

print(data)

print(data['data'][0])

alcohol.close()