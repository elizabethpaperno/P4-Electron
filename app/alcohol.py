import json

alcohol = open('app/datasets/alcohol.json')

data = json.load(alcohol)

#print(data)

print(data['data'][0])

p_name = []
mode = []
address = []

for res in data['data']:
    p_name.append(res[13])
    mode.append(res[22])
    address.append(str(res[15]) + ' ' + str(res[19]))

print(address)
alcohol.close()

def get_name():
    return p_name

def get_mode():
    return mode

def get_address():
    return address