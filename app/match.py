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

data = [
    #name       TEXT
    #address    TEXT
    #zip        INT
    #alcohol    BOOL
    #sanitation INT
]

def assembleDB() :
    yelp_data = json.load(open('yelp.json'))

    #get all data in Manhattan restaurants
    alcohol_data = list(json.load(open('app/static/js/datasets/alcohol.json', encoding='UTF-8'))['data'])
    new_alcohol_data = []
    for rest in alcohol_data:
        if (rest[9] == "NEW YORK") and ("RESTAURANT" in str(rest[22])):
            new_alcohol_data.append(rest)
    
    #print(new_alcohol_data[0])

    sanitation_data = list(json.load(open('app/static/js/datasets/sanitation.json', encoding='UTF-8'))['data'])
    new_sanitation_data = []
    for rest in sanitation_data:
        if rest[9] == "Manhattan":
            new_sanitation_data.append(rest)

    #print(new_sanitation_data[0])

    restaurants = yelp_data['name']
    addresses = yelp_data['address']
    zip_codes = yelp_data['zip_code']

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

            restaurant = [name, address, alcohol, sanitation]
            data.append(restaurant)
        except KeyError:
            print("key error for " + str(i))
            continue
        
    print(data)

    #other notable keys: latitude, longitude, zip_code
    #in alcohol.json, zip is index 19, city is index 9, address is index 15, name is index 13, method of operation is index 22
    #in sanitation.json, zip is index 12, address is index 10 + 11, name is index 8, borough is index 9, inspection date is index 18

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

    for rest in new_sanitation_data:
        #use zip code to lower the sample size
        input_address = str(address).lower()
        comparing_address = shortenAddress((str(rest[10]) + " " + str(rest[11])).lower())

        if input_address == comparing_address:
            #print("perfect match for " + name + " at " + address)
            return rest[16]
        else:
            try:
                if (str(zip) == (str(rest[12]))):
                    #see how closely the name and address match
                    input_name = str(name).lower()
                    comparing_name = (str(rest[8]).lower())
                    name_match = SequenceMatcher(None, input_name, comparing_name).ratio()
                    #print(input_name + " and " + comparing_name + " have a similarity ratio of " + str(name_match))

                    address_match = SequenceMatcher(None, input_address, comparing_address).ratio()
                    #if both the name and the address are 75% similar to each other
                    if (name_match > .5) and (address_match > .75):
                        # print("matched " + input_name + " with " + comparing_name)
                        # print("matched " + input_address + " with " + comparing_address)
                        return rest[16]
                    # else:
                        # print("rejected " + input_name + " == " + comparing_name)
                        # print("rejected " + input_address + " == " + comparing_address)                    
            except ValueError:
                continue

    # print("found no match for " + name + " at " + address)
    return -1

def removeStrings(string):
    list = str.split(string)
    if (list[len(list) - 1] in SHORTEN_STRINGS):
        del list[len(list) - 1]
    return " ".join(list)

def shortenAddress(address):
    list = str.split(address)
    for i in range(len(list)):
        if list[i] in SHORTEN_STRINGS:
            list[i] = SHORTEN_STRINGS[list[i]]
            
    return " ".join(list)

#print(shortenAddress("98 mott boulevard"))
assembleDB()

#open JSON as Python dict
#addresses are shortened ex: 22A ORCHARD ST
# alcohol = open('app/static/js/datasets/alcohol.json', encoding='UTF-8')
# a_data = json.load(alcohol) 
# for restaurant in a_data['data'] :
#     if restaurant[17] == "NEW YORK":
#         print(restaurant)
#         break

# #addresses are full expanded ex: 125 EAST AVENUE
# sanitation = open('app/static/js/datasets/sanitation.json', encoding='UTF-8')
# s_data = json.load(sanitation)['data']
# print(s_data[0][18])
# print(s_data[0][18] < "2013-07-15T00:00:00")
# for restaurant in s_data['data'] :
#     # if (restaurant[9] == "Manhattan") :
#     #     print(restaurant)
#     #     break
#     address = str(restaurant[10]) + " " + str(restaurant[11])
#     if "500 grand st" in (address.lower()):
#         print(restaurant)
#         s = SequenceMatcher(None, "500 grand st", address.lower())
#         print(s.ratio())
#         break

# yelp = open("yelp.json")
# y_data = json.load(yelp)
# print(y_data['name']['0'])
# print(y_data['address']['0'])
#print(y_data.keys())
#print(y_data['address'])

# print(data.keys())
# print(data['data'][0])