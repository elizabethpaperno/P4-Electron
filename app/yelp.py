import json
import requests
import pickle
import pandas as pd
import numpy as np

## Define function to gather keys:
with open("app/keys/key_api1") as f:
    API_KEY_ID = f.read().strip()

url = "https://api.yelp.com/v3/businesses/search"
key = API_KEY_ID


## Identify headers:
headers = {'Authorization': 'Bearer {}'.format(key)}

neighborhoods = ['Midtown West', 'Greenwich Village', 'East Harlem', 'Upper East Side', 'Midtown East',
                 'Gramercy', 'Little Italy', 'Chinatown', 'SoHo', 'Harlem',
                 'Upper West Side', 'Tribeca', 'Garment District', 'Stuyvesant Town', 'Financial District',
                'Chelsea', 'Morningside Heights', 'Times Square', 'Murray Hill', 'East Village',
                'Lower East Side', 'Hell\s Kitchen', 'Central Park']

def getYelpJson():

    nyc = [[] for i in range(len(neighborhoods))]

    #Function to draw in data for each neighborhood:
    for x in range(len(neighborhoods)):
        print('---------------------------------------------')
        print('Gathering Data for {}'.format(neighborhoods[x]))
        print('---------------------------------------------')


        for y in range(20):
            location = neighborhoods[x]+', Manhattan, NY'
            term = "Restaurants"
            search_limit = 50
            offset = 50 * y
            categories = "(restaurants, All)"
            sort_by = 'distance'

            url_params = {
                            'location': location.replace(' ', '+'),
                            'term' : term,
                            'limit': search_limit,
                            'offset': offset,
                            'categories': categories,
                            'sorty_by': sort_by
                        }

            response = requests.get(url, headers=headers, params=url_params)
            print('***** {} Restaurants #{} - #{} ....{}'.format(neighborhoods[x], offset+1, offset+search_limit,  response))
            nyc[x].append(response)


    print(response)
    print(type(response.text))
    print(response.json().keys())
    print(response.text[:1000])

    # Save the compiled data into dataframe and remove any empty data:
    df = pd.DataFrame()
    for x in range(len(neighborhoods)):
        if x == 6: # Little Italy has a total of 486 restaurants
            for y in range(10):
                df_temp = pd.DataFrame.from_dict(nyc[x][y].json()['businesses'])
                df_temp.loc[:,'neighborhood'] = neighborhoods[x]
                df = df.append(df_temp)
        if x == 13: # Stuyvesant Town has a total of 417 restaurants
            for y in range(10):
                df_temp = pd.DataFrame.from_dict(nyc[x][y].json()['businesses'])
                df_temp.loc[:,'neighborhood'] = neighborhoods[x]
                df = df.append(df_temp)

        else:
            for y in range(20):
                df_temp = pd.DataFrame.from_dict(nyc[x][y].json()['businesses'])
                if len(df_temp) !=  0:
                    df_temp.loc[:,'neighborhood'] = neighborhoods[x]
                df = df.append(df_temp)

    #print(len(df))
    #df.head()

    # Add a column that counts how many data entries have the same id (and therefore represent the same restaurant):
    df['count'] = df.groupby('id')['id'].transform('count')

    # Sort values by name and id:
    df_sorted = df.sort_values(by=['alias', 'id'])

    # Drop duplicate values:
    df_filtered = df_sorted.drop_duplicates(subset=['alias', 'id'], keep='first', inplace=False).copy()

    # Double check no duplicates remain:
    df_filtered['count'] = df_filtered.groupby('id')['id'].transform('count')
    print('# of Restaurants in Manhattan: ', len(df_filtered))
    print('# of duplicates: ', len(df_filtered[df_filtered['count'] > 1]))
    df_filtered.reset_index(inplace=True, drop = True)
    #df_filtered.head()

    # Remove columns that we will not be working with:
    #df_filtered.drop(columns = ['alias', 'distance', 'id', 'image_url', 'is_closed', 'phone', 'url','count'], inplace = True, axis=1)

    # Extract dictionary values for the category, latitude, longitude, and location:
    df_filtered['categories_clean'] = df_filtered['categories'].apply(lambda a: [x['alias'] for x in a])
    df_filtered['latitude'] = df_filtered['coordinates'].apply(lambda x: x.get('latitude'))
    df_filtered['longitude'] = df_filtered['coordinates'].apply(lambda x: x.get('longitude'))
    df_filtered['address'] = df_filtered['location'].apply(lambda x: x.get('address1'))
    df_filtered['city'] = df_filtered['location'].apply(lambda x: x.get('city'))
    df_filtered['zip_code'] = df_filtered['location'].apply(lambda x: x.get('zip_code'))
    df_filtered['state'] = df_filtered['location'].apply(lambda x: x.get('state'))

    # Remove original categories, coordinates, and location columns:
    df_filtered.drop(columns=['categories','coordinates', 'location'], inplace = True, axis=1)

    # Get dummy variables for categorical columns (categories and transactions):
    categories_dummy = df_filtered['categories_clean'].str.join(sep=',').str.get_dummies(sep=',')
    transactions_dummy = df_filtered['transactions'].str.join(sep=',').str.get_dummies(sep=',')

    # Combine new columns with original dataframe:
    df_filtered = pd.concat([df_filtered, categories_dummy, transactions_dummy], axis=1)
    df_filtered.head()

    # Add in number of categories:
    #df_filtered['num_of_cat'] = df_filtered['categories_clean'].apply(lambda x: len(x))

    # Find the most frequent categories (anything with over 150 entries):
    #all_category = pd.DataFrame(categories_dummy.sum().sort_values(ascending=False))
    #category = list(all_category[all_category[0] > 150].index)

    # Identify each restaurant as either being a mainstream or a rare category:
    # df_filtered['mainstream_category'] = np.sum(df_filtered[category], axis = 1)
    # df_filtered['rare_category'] = 0
    # df_filtered.loc[df_filtered['mainstream_category'] == 0, 'rare_category'] = 1
    # df_filtered.loc[df_filtered['mainstream_category'] != 0, 'mainstream_category'] = 1

    # Replace null values in the price column with 'zero'
    df_filtered['price'].fillna(value='N/A', inplace=True)

    # Update price to be numerical values:
    price = {'$': 1, '$$': 2, '$$$':3, '$$$$': 4, 'N/A': 0}
    df_filtered['price_value'] = df_filtered['price'].map(price)

    # Remove null values from latitude, longitude, and address columns:
    df_filtered.dropna(inplace=True)

    # get rid of NJ resturants and any other resturants not in NYS that may have been picked up by the search
    # df_filtered =  df_filtered[df_filtered["state"] == "NY"]

    # add column that includes full adresses
    # df_filtered["formatted_address"] = df_filtered.apply(lambda row: row.address + ", " + row.city + ", " + row.state + " " + row.zip_code, axis=1)
    df_filtered.to_json("yelp.json")

# df = getYelpDB()
# print(len(df))

# print(df.count())
# print(df.head())
# print(list(df.columns.values))
# print(df["categories_clean"])

def editDF(df):
    # get rid of NJ resturants and any other resturants not in NYS that may have been picked up by the search
    df =  df[df["state"] == "NY"]
    # add column that includes full adresses
    df["formatted_address"] = df.apply(lambda row: row.address + ", " + row.city + ", " + row.state + " " + row.zip_code, axis=1)
    df["cords"] = df.apply(lambda row: [row.latitude, row.longitude] , axis=1)
    return df

def getName(df, address):
    df_filt = df[df["formatted_address"] == address]
    return (df_filt.iloc[0]['name'])

def getRating(df, address):
    df_filt = df[df["formatted_address"] == address]
    return (df_filt.iloc[0]['rating'])

def getFormattedCategories(df, address):
    df_filt = df[df["formatted_address"] == address]
    return (', '.join(df_filt.iloc[0]['categories_clean']))

def getPrice(df, address):
    df_filt = df[df["formatted_address"] == address]
    if(df_filt.iloc[0]['price_value'] != "N/A"):
        return (int(df_filt.iloc[0]['price_value'])* "$")
    else:
        return ("price not available")

def getDelieveryYN(df, address):
    df_filt = df[df["formatted_address"] == address]
    if(df_filt.iloc[0]['delivery'] == 1):
        return ("delivery available")
    else:
        return ("delivery not available")

def getPickupYN(df, address):
    df_filt = df[df["formatted_address"] == address]
    if(df_filt.iloc[0]['pickup'] == 1):
        return ("takeout available")
    else:
        return ("pickup not available")

def getFullFormattedAddress(df,address):
    df_filt = df[df["address"] == address]
    state = df_filt.iloc[0]['state']
    city = df_filt.iloc[0]['city']
    zip = df_filt.iloc[0]['zip_code']
    return (address + ", " + city + ", " + state + " " + zip)


def getImgUrl(df,address):
    df_filt = df[df["formatted_address"] == address]
    try:
        return (df_filt.iloc[0]['image_url'])
    except:
        return "no img available"

def getListAllAddresses(df):
    return(df["formatted_address"].values.tolist())

#not yet working
def getFilteredListAddresses(df, filters):
    df_filt = df
    for i in filters:
        df_filt = df_filt[df_filt[i] == 1]
    return(df_filt["formatted_address"].values.tolist())

def getListAllCords(df):
    return(df["cords"].tolist())

def getShortAddress(df, full_address):
    df_filt = df[df["formatted_address"] == full_address]
    return (df_filt.iloc[0]['address'])

def getTopCats(df):
    categories_dummy = df['categories_clean'].str.join(sep=',').str.get_dummies(sep=',')
    all_category = pd.DataFrame(categories_dummy.sum().sort_values(ascending=False))
    category = list(all_category[all_category[0] > 100].index)
    #print(category)

if __name__ == "__main__":
    # getYelpJson()
    df = pd.read_json("yelp.json")
    df = editDF(df)
    print(getTopCats(df))
    print(df.info())
    #print(df["city"].unique())
    print(getFullFormattedAddress(df, "12 E 32nd St"))
    #print(getListAllCords(df))
    print(getName(df, "12 E 32nd St, New York, NY 10016"))
    print(getRating(df, "12 E 32nd St, New York, NY 10016"))
    print(getFormattedCategories(df, "12 E 32nd St, New York, NY 10016"))
    print(getPrice(df,"12 E 32nd St, New York, NY 10016"))
    print(getDelieveryYN(df,"12 E 32nd St, New York, NY 10016"))
    print(getPickupYN(df,"12 E 32nd St, New York, NY 10016"))
    print(getImgUrl(df,"12 E 32nd St, New York, NY 10016"))
    #print(getFilteredListAddresses(df,["tacos"]))
    #print(getListAllAddresses(df))
