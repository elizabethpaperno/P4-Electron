function initMap() {
    const myLatLng = { lat: 40.7178, lng: -74.0138 };
    const myLatLng1 = { lat: 40.7278, lng: -74.0138 };
    const myLatLng2 = { lat: 40.7378, lng: -74.0138 };
    
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: myLatLng,
    });
    
    map.setOptions({ styles: styles["hide"] });
  
    new google.maps.Marker({
      position: myLatLng,
      map,
      title: "Hello World!",
    });
    new google.maps.Marker({
      position: myLatLng1,
      map,
      title: "Hello World!",
    });
    new google.maps.Marker({
      position: myLatLng2,
      map,
      title: "Hello World!",
    });
    new google.maps.Marker({
      position: myLatLng,
      map,
      title: "Hello World!",
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