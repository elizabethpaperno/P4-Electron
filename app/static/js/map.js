  var geocoder;
  var map;
  function initialize() { // create map
    const newYork = { lat: 40.7128, lng: -74.0060}; // nyc is center of the map
    //const myLatLng1 = { lat: 40.7278, lng: -74.0138 };
    //const myLatLng2 = { lat: 40.7378, lng: -74.0138 };
    const school = "345 Chambers St, New York, NY 10282"
    geocoder = new google.maps.Geocoder();
    
    var mapOptions = { //holds map center
      zoom: 10,
      center: newYork
    }
    
    map = new google.maps.Map(document.getElementById('map'), mapOptions); // create map
    map.setOptions({ styles: styles["hide"] }); //hide annoying map features
    
    codeAddress(school)
  }

  function codeAddress(point) {
    var address = point;
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == 'OK') {
        map.setCenter(results[0].geometry.location);
        return marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
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
  
  window.initMap = initMap;

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