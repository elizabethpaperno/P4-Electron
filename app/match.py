import json
try:
    from db import query_db
except:
    from db import query_db

from difflib import SequenceMatcher

REMOVE_STRINGS = ['llc', 'inc', 'corp']
SHORTEN_STRINGS = {
    'avenue' : 'ave',
    'street' : 'st',
    'north' : 'n',
    'east' : 'e',
    'south' : 's',
    'west' : 'w',
    'boulevard' : 'blvd',
    'place' : 'pl'
}

data = {
    #address : {"alcohol" : true, "score" : int}
}

def createSanitation():
    sanitation_data = list(json.load(open('app/static/js/datasets/sanitation.json', encoding='UTF-8'))['data'])
    new_sanitation_data = {}
    for rest in sanitation_data:
        zip = rest[12]
        borough = rest[9]
        address = shortenAddress(str(rest[10]) + " " + str(rest[11]))
        inspection_date = rest[18]
        if borough == "Manhattan" :
            # if from a new zip code
            if not zip in new_sanitation_data:
                # create new inner dict
                inner_dict = {address : rest}
                new_sanitation_data.update({zip : inner_dict})
            # if from an old zip code
            else:
                # update inner dict
                inner_dict = dict(new_sanitation_data[zip])
                # check if the address already exists in inner_dict
                if address in inner_dict:
                    # if the address already exists, only update if the inspection date is newer
                    if (inspection_date > inner_dict[address][18]):
                        inner_dict.update({address : rest})
                        new_sanitation_data.update({zip : inner_dict})
                # if the address does not already exist, add it
                else:
                    inner_dict.update({address : rest})
                    new_sanitation_data.update({zip : inner_dict})
    return new_sanitation_data

def assembleDB() :
    print("now assembling sanitation and alcohol data")    

    yelp_data = json.load(open('yelp.json'))

    #get all data in Manhattan restaurants
    alcohol_data = list(json.load(open('app/static/js/datasets/alcohol.json', encoding='UTF-8'))['data'])
    new_alcohol_data = []
    for rest in alcohol_data:
        if (rest[9] == "NEW YORK") and ("RESTAURANT" in str(rest[22])):
            new_alcohol_data.append(rest)
    
    #print(new_alcohol_data[0])

    new_sanitation_data = createSanitation()

    restaurants = yelp_data['name']
    addresses = yelp_data['address']
    zip_codes = yelp_data['zip_code']

    ten_percent = len(restaurants) // 10

    for i in range(len(restaurants)):
        try:
            name = restaurants[str(i)]
            #print(name)
            address = addresses[str(i)]
            #print(address)
            zip = zip_codes[str(i)]
            #print(zip)
            alcohol = hasAlcohol(name, address, zip, new_alcohol_data)
            sanitation = getSanitationScore(name, address, zip, new_sanitation_data)

            restaurant = {address : {'alcohol' : alcohol, 'score' : sanitation, 'name' : name}}
            data.update(restaurant)

            if (i % ten_percent == 0):
                progress = (i / ten_percent) * 10
                print(str(progress) + "%")

        except KeyError:
            #print("key error for " + str(i))
            continue
        
    with open("sanitation_alcohol.json", "w") as fp:
        json.dump(data, fp)

    #other notable keys: latitude, longitude, zip_code
    #in alcohol.json, zip is index 19, city is index 9, address is index 15, name is index 13, method of operation is index 22
    #in sanitation.json, zip is index 12, address is index 10 + 11, name is index 8, borough is index 9, inspection date is index 18
    # score is index 16

#looks for a restaurant in the same zip code, and with a similar name and address
def hasAlcohol(name, address, zip, new_alcohol_data):
    # highest_name_ratio = 0
    # highest_address_ratio = 0

    for rest in new_alcohol_data:
        if str(rest[15]).lower() == str(address).lower():
            #print("alcohol at " + address)
            return True
        else:
            #use zip code to lower the sample size
            try:
                #print("comparing " + str(zip) + " vs " + str(rest[19]))
                if (str(zip) == (str(rest[19]))):
                    #see how closely the name and address match
                    input_name = str(name).lower()
                    comparing_name = removeStrings(str(rest[13]).lower())
                    name_match = SequenceMatcher(None, input_name, comparing_name).ratio()
                    #print(input_name + " and " + comparing_name + " have a similarity ratio of " + str(name_match))


                    input_address = str(address).lower()
                    comparing_address = str(rest[15]).lower()
                    address_match = SequenceMatcher(None, input_address, comparing_address).ratio()
                    #print(input_address + " and " + comparing_address + " have a similarity ratio of " + str(address_match))

                    #if both the name and the address are similar to each other
                    if (name_match > .6) and (address_match > .95):
                        # print("alcohol detected")
                        # print("matched " + input_name + " with " + comparing_name)
                        # print("matched " + input_address + " with " + comparing_address)
                        return True
            except ValueError:
                continue
    return False

def getSanitationScore(name, address, zip, new_sanitation_data):

    sample = dict(new_sanitation_data[str(zip)])
    addresses = sample.keys()
    input_address = str(address).lower()
    input_name = str(name).lower()

    if input_address in addresses:
        # print("perfect match for " + name + " at " + input_address)
        return sample[input_address][16]
    else:
        for address in addresses:
            address_similarity = SequenceMatcher(None, input_address, address).ratio()
            comparing_name = shortenAddress(str(sample[address][8]))
            name_similarity = SequenceMatcher(None, input_name, comparing_name).ratio()

            if (name_similarity > .5) and (address_similarity > .75):
                # print("matched " + input_name + " with " + comparing_name)
                # print("matched " + input_address + " with " + address)
                return sample[address][16]
    # print("could not find match for " + input_address + " at " + input_name)
    return -1

def removeStrings(string):
    list = str.split(string)
    if (list[len(list) - 1] in SHORTEN_STRINGS):
        del list[len(list) - 1]
    return " ".join(list)

def shortenAddress(address):
    lowercase_address = str(address).lower()
    list = str.split(lowercase_address)
    for i in range(len(list)):
        if list[i] in SHORTEN_STRINGS:
            list[i] = SHORTEN_STRINGS[list[i]]
            
    return " ".join(list)

def getGrade(address, data):
    if not address in data:
        return "No sanitation data available"
    
    score = int(data[address]['score'])
    grade = "A"

    if score < 0:
        return "No sanitation data available"
    if score > 13:
        grade = "B"
    if score > 27:
        grade = "C"
    return "Sanitation grade: " + grade

def getAlcohol(address, data):
    return "Alcohol: " + str(address in data)

#print(shortenAddress("98 mott boulevard"))
# data = assembleDB()
# print(data.keys())
# print(data['49 Clinton St'])
# print(getGrade("49 Clinton St", data))
# print(getAlcohol("49 Clinton St", data))