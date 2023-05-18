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
    const school = "345 Chambers St, New York, NY 10282"
    geocoder = new google.maps.Geocoder();
    
    var mapOptions = { //holds map center
      zoom: 10,
      center: newYork
    }
    
    map = new google.maps.Map(document.getElementById('map'), mapOptions); // create map
    map.setOptions({ styles: styles["hide"] }); //hide annoying map features
    
    var a = codeAddress(school)
    //a.addListener("click", blah);
    //console.log(a.getClickable())
  }
  
  var blah = () => {
    console.log("clicked")
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
        a.addListener("click", blah)
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