var geocoder;
var map;
var start = 0;
var end = 100;
var listLength;
var finalList = [];
var markerList = [];

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
  const alcoholPlace = document.getElementById("restAlcohol")
  const sanitationPlace = document.getElementById("restSanitation")
  const resForm = document.getElementById("saveRestaurantForm")
  
  widgetArea.style.display = "block"

  var data = title.split(",")

  //console.log(title.split())

  // creating string splices
  const name = data.shift()
  const rating = data.shift()
  var cats = ""
  // console.log(name)
  // console.log(rating)
  
  var skip = true
  var price= "Price not available"
  for (var i = 0; i < data.length; i=i){
    if (data[i].includes("$")) {break}
    else if (data[i].includes("delivery")) {
      skip = false
      break
    }
    if (data[i]===" " || data[i]==="") {data.shift()}
    else if (data[i+1].includes("delivery")) {
      cats += data.shift()
    }
    else {
      cats += data.shift() + ", "}
  }

  if (skip) {price = data.shift()}
  const delivery = data.shift()
  const pickup = data.shift()
  const img = data.shift()
  const sanitation = data.shift()
  const alcohol = data.shift()
  var location = ""
  for (var i = 0; i < data.length; i=i){
    location += data.shift()
    //console.log(location)
    if (data.length===0){
      
    }
    else {
      location +=","
    }
  }

  namePlace.innerHTML=name;
  ratingPlace.innerHTML=rating;
  catPlace.innerHTML=cats
  pricePlace.innerHTML = price;
  deliveryPlace.innerHTML = delivery
  pickupPlace.innerHTML = pickup
  locationPlace.innerHTML = location
  imgPlace.src=img
  alcoholPlace.innerHTML = alcohol
  sanitationPlace.innerHTML = sanitation
  
  const saveButton = document.getElementById("addRes")
  var saving = (sb)=> {
    var toSave = document.getElementById("favoriteRestaurant");
    toSave.value = location;
    //console.log("name: " + location)
    sb.removeEventListener("click", saving)
    sb.type="submit"
    //resForm.action = "/addRestaurant"
    sb.submit()
    
    
  }
  
  saveButton.addEventListener("click" , ()=>{
    saving(saveButton)
  })
  
  
  
  
  // console.log(cats)
  // console.log(data)
  // console.log(location)

  //deleteNodes(widgetArea)


  //const node = document.createTextNode("Onclick works");
  // widgetArea.appendChild(node)
  // //this was a test and it works
  // //const cardParent =
  //console.log(title)
  //createLikedRestTable()
  //addRestaurant("blah",location)
  //preparePayload() 
}

function preparePayload(){
  var payload = ""
  for (var i = 0; i < finalList.length; i++){
    for (var j = 0; j < finalList[i].length;j++){
      if (j===finalList[i].length-1) {payload += finalList[i][j] + 'rsuf'}
      else {payload += finalList[i][j] + '!'}
    }
  }
  //console.log(payload)
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
      markerList.push(a)
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

  var pageNumber = parseInt(document.getElementById("pageNumber").value, 10)
  end = 100 * pageNumber
  start = 100 * (pageNumber - 1)

  finalList= []

  for (var i = 0; i < list.length; i++){
    restaurant = list[i]
    meta = restaurant.split("!")
    finalList.push(meta)
  }
  //console.log(finalList)
  //console.log(finalList)

  //console.log(list)

  //var i = 0;

  //var stop = 100;

  local_end = end

    if (local_end > listLength) {
        local_end = listLength
    }

  listLength = list.length
  
  //console.log(finalList)
  
  for (var i = 0; i < local_end ; i++) {
    console.log(typeof finalList[i])
    console.log(i)
    codeAddress(finalList[i]);
    sleep(1000);
    //console.log(list[i])
  }

  // list.forEach(address => {
  //     codeAddress(address)
  //     sleep("1000")

  // });
});

// console.log(listLength)
// console.log(start)
// console.log(end)
function switchPage() {
    //delete markers
    for (let i = 0; i < markerList.length; i++) {
        markerList[i].setMap(null);
    } 
    markerList = []

    local_end = end

    if (local_end > listLength) {
        local_end = listLength-1
    }
    
    //console.log(local_end)
    // undefined error is caused by wrong index of local end

    for (let i = start; i < local_end; i++){
        codeAddress(finalList[i])
        sleep(1000)
    }

    displayPageNumber = document.getElementById("displayPageNumber")
    displayPageNumber.innerHTML = "Page " + (end / 100)
}

function nextPage() {
    // console.log(listLength)
    // console.log(start)
    // console.log(end)
    //console.log(start + 100 < listLength)
    var lLength = listLength-1
    if (start + 100 < lLength) {
        start = start + 100
        end = end + 100
    }

    console.log("start: ", start)
    console.log("stop: ", end)
    switchPage()
}

function previousPage() {
  
    if (end > 100){
        start = start - 100
        end = end - 100
    }

    console.log("start: ", start)
    console.log("stop: ", end)
    switchPage()
}

function getPageNumber() {
    pageNumber = document.getElementById("pageNumber")
    pageNumber.value = end / 100
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
