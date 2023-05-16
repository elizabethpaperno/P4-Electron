//set up map
var map = L.map('map').setView([40.7831, -73.9712], 13);

L.tileLayer('https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg', {
    maxZoom: 19,
}).addTo(map);

