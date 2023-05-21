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

var createWidget = () => {
  const widgetArea = document.getElementById("restWidget");
  deleteNodes(widgetArea)
  // const node = document.createTextNode("This is new.");
  // widgetArea.appendChild(node)
  // this was a text and it works
  //const cardParent = 
  
}

function deleteNodes(element) {
  while (element.firstChild){
    element.removeChild(element.firstChild)
  }
}

function codeAddress(point) {
  var address = point;
  var marker;
  marker = geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == 'OK') {
      map.setCenter(results[0].geometry.location);
      var a = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
          optimized: false
      });
      a.addListener("click", createWidget)
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
  var addresses = document.getElementById("data").className
  var list = addresses.split(";")
  console.log(list)
  
  //var i = 0;
  
  var stop = 100;
  
  if (list.length < 100) {
    stop = list.length
  }
  
  
  for (var i = 0; i < stop; i++) {
    codeAddress(list[i]);
    sleep(1000);
    //console.log(list[i])
  }
  
  // list.forEach(address => {
  //     codeAddress(address)
  //     sleep("1000")
      
  // });
});

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