console.log("running map_leaflet.js")

window.addEventListener("load", (event) => {
    //convert string to list
    var addresses = document.getElementById("data").className
    var list = addresses.split(",")
    console.log(list)

    // list.forEach(address => {
    //     addMarker(address)
    //     sleep("1000")
    // });
});

function addMarker(coordinates) {
    var marker  = L.marker(coordinates).addTo(map)
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
