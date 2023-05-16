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
  var geocoder;
  var map;
  function initialize() {
    const newYork = { lat: 40.7128, lng: -74.0060};
    //const myLatLng1 = { lat: 40.7278, lng: -74.0138 };
    //const myLatLng2 = { lat: 40.7378, lng: -74.0138 };
    const school = "345 Chambers St, New York, NY 10282"
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(-34.397, 150.644);
    var mapOptions = {
      zoom: 10,
      center: newYork
    }
    
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    map.setOptions({ styles: styles["hide"] });
    
    codeAddress(school)
  }

  function codeAddress(point) {
    var address = point;
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == 'OK') {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location
        });
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
  }

  
function addMarker(lat,long) {
  if (!(typeof lat == "string" && typeof long=="string")) {
    return "nothing"
  } else {
    return new google.maps.Map(document.getElementById("map"), {
      center: {lat: lat, lng: long},
    });
  }
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