var geocoder;
var map;

async function initialize() { // create map
  // Request needed libraries.
const { Map, InfoWindow } = await google.maps.importLibrary("maps");
const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
  "marker"
);


  const newYork = { lat: 40.7128, lng: -74.0060}; // nyc is center of the map
  //const myLatLng1 = { lat: 40.7278, lng: -74.0138 };
  //const myLatLng2 = { lat: 40.7378, lng: -74.0138 };
  //const school = "345 Chambers St, New York, NY 10282"
  geocoder = new google.maps.Geocoder();

  var mapOptions = { //holds map center
    zoom: 10,
    center: newYork
  }

  map = new google.maps.Map(document.getElementById('map'), mapOptions); // create map
  map.setOptions({ styles: styles["hide"] }); //hide annoying map features

  //var a = codeAddress(school)
  //a.addListener("click", blah);
  //console.log(a.getClickable())
}

var createWidget = (title) => {
  const widgetArea = document.getElementById("restWidget");
  const namePlace = document.getElementById("restName")
  const ratingPlace = document.getElementById("restRating")
  const catPlace = document.getElementById("restCats")
  const pricePlace = document.getElementById("restPrice")
  const deliveryPlace = document.getElementById("restDelivery")
  const pickupPlace = document.getElementById("restPickup")
  const imgPlace = document.getElementById("restImg")
  const locationPlace = document.getElementById("restLocation")

  var data = title.split(",")

  //console.log(title.split())

  // creating string splices
  const name = data.shift()
  const rating = data.shift()
  var cats = ""
  console.log(name)
  console.log(rating)


  for (var i = 0; i < data.length; i=i){
    if (data[i].includes("$")) {break}
    cats += data.shift() + ", "
  }

  const price = data.shift()
  const delivery = data.shift()
  const pickup = data.shift()
  const img = data.shift()
  var location = ""
  for (var i = 0; i < data.length; i=i){
    location += data.shift()
  }

  namePlace.innerHTML=name;
  ratingPlace.innerHTML=rating;
  catPlace.innerHTML=cats
  pricePlace.innerHTML = price;
  deliveryPlace.innerHTML = delivery
  pickupPlace.innerHTML = pickup
  locationPlace.innerHTML = location
  imgPlace.src=img



  console.log(cats)
  console.log(data)
  console.log(location)



  //deleteNodes(widgetArea)


  //const node = document.createTextNode("Onclick works");
  // widgetArea.appendChild(node)
  // //this was a test and it works
  // //const cardParent =
  //console.log(title)
}

function deleteNodes(element) {
  while (element.firstChild){
    element.removeChild(element.firstChild)
  }
}

function codeAddress(data) {
  var address = data[data.length-1];
  var marker;
  marker = geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == 'OK') {
      //map.setCenter(results[0].geometry.location);
      var a = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
          title: data.toString(),
          optimized: false
      });
      a.addListener("click", ()=>{createWidget(a.getTitle())})
      //console.log(a)
      //a.setClickable(true)
      return a;

    } else {
      console.log('Geocode was not successful for the following reason: ' + status);
    }
  });
  //console.log(typeof marker)
  return marker;
}

const styles = {
  default: [],
  hide: [
    {
      featureType: "poi",
      stylers: [{ visibility: "off" }],
    },
    {
      featureType: "transit",
      elementType: "labels.icon",
      stylers: [{ visibility: "off" }],
    },
  ],
};

window.initMap = initialize;

// Restaurant Data Holder
class Restaurant {
  constructor(name, address, link, rating, category, alcohol) {
    this.name = name;
    this.address = address;
    this.link = link;
    this.rating = rating;
    this.category = category;

  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

//PLEASE DO NOT USE THIS (IT WORKS THOUGH)
window.addEventListener("load", (event) => {
  //convert string to list
  var addresses = document.getElementById("data").value
  var list = addresses.split("rsuf")
  //console.log(list)
  var finalList= []

  for (var i = 0; i < list.length; i++){
    restaurant = list[i]
    meta = restaurant.split("!")
    finalList.push(meta)
  }
  //console.log(finalList)

  //console.log(list)

  //var i = 0;

  var stop = 100;

  if (list.length < 100) {
    stop = list.length
  }

  for (var i = 0; i < stop; i++) {
    codeAddress(finalList[i]);
    sleep(1000);
    //console.log(list[i])
  }

  // list.forEach(address => {
  //     codeAddress(address)
  //     sleep("1000")

  // });
});

const sqlite3 = require('sqlite3').verbose();

function query(sqlstr) {
  let db = new sqlite3.Database('P4-Electron/P4.db', (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the liked resturant database.');
  });
  let sql = sqlstr;
  db.run(sql)
  db.close((err) => {
  if (err) {
    console.error(err.message);
  }
    console.log('Close the database connection.');
  });
}

def createLikedRestTable(){
  query("CREATE TABLE IF NOT EXISTS liked_rest(username TEXT PRIMARY KEY, rest_name TEXT)")
}

def addRestaurant(user,rest_name){
  query('INSERT INTO liked_rest VALUES (' + user + ', ' + rest_name ");")
}

def getLikedRestaurants(user){
  list = []
  let db = new sqlite3.Database('./P4.db', (err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Connected to the liked resturant database.');
  });
  let sql = 'SELECT rest_name FROM liked_rest WHERE user = ' + user + ';'
  db.all(sql, [], (err, rows) => {
  if (err) {
    throw err;
  }
  rows.forEach((row) => {
    list.push(row.res_name);
    });
  });
  db.close();
  console.log(list)
}

/*
TODO: ADD the new categories

*/


// function initMap() {
//     const newYork = { lat: 40.7128, lng: -74.0060};
//     const myLatLng1 = { lat: 40.7278, lng: -74.0138 };
//     const myLatLng2 = { lat: 40.7378, lng: -74.0138 };
//     const school = "345 Chambers St, New York, NY 10282"

//     const map = new google.maps.Map(document.getElementById("map"), {
//       zoom: 10,
//       center: newYork
//     });

//     map.setOptions({ styles: styles["hide"] });

//     new google.maps.Marker({
//       position: school,
//       map,
//       title: "Hello World!",
//     });

//   }

// function addMarker(lat,long) {
//   if (!(typeof lat == "string" && typeof long=="string")) {
//     return "nothing"
//   } else {
//     return new google.maps.Map(document.getElementById("map"), {
//       center: {lat: lat, lng: long},
//     });
//   }
// }
