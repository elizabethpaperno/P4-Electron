#  Restaurant Surfer by Where Are The Electrons?
## PM: Elizabeth Paperno
## Devo: Jeffery Tang 
## Devo: Kevin Li
## Devo: Abid Talukder

## Summary
Restaurant Surfers incorporates datasets about restaurants to provide users the ability to find their dream restaurant. Users can filter by food type, dietary restrictions, parking, takeout, delievery, and more. Users can also view restaurants on an embedded map and publish reviews and view Yelp rating and price. 
## APIs
- [Embedded Google Maps API](https://developers.google.com/maps/documentation/embed/get-started)
## Datasets
- [Yelp](https://www.yelp.com/dataset/documentation/main)
- [Active alcohol permits](https://data.ny.gov/Economic-Development/Liquor-Authority-Current-List-of-Active-Licenses/hrvs-fxs2/data)
- [NYC Sanitation Grades](https://data.cityofnewyork.us/Health/Restaurant-Grades/gra9-xbjk/data)
## How to Clone, Install, and Run

`0) Create and activate an environment`
```
python3 -m venv <<name>>
cd <<name>>
. bin/activate
```
`1) Clone the project `
```
git clone git@github.com:elizabethpaperno/P4-Electron.git
```

`2) Navigate to root directory`

``` 
cd P4-Electron/
```
`3) install requirements`
```
pip install -r requirements.txt
```
`4) Run the program`

``` 
python3 app/__init__.py
```

`5) Open the following link in any web browser`
```
https://127.0.0.1:5000
