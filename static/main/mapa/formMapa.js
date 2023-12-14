
var user_location = [-8.42565,125.32489084];
    var map = L.map('map').setView(user_location, 8);

    L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
                  attribution: 'Google Maps',
                  maxZoom: 20,
                  subdomains:['mt0','mt1','mt2','mt3']
                  }).addTo(map);

    
    
    


var popup = L.popup();
var marker = L.marker();

function onMapClick(e) {
    marker.setLatLng(e.latlng).addTo(map)
        .bindPopup("You clicked the map at " + e.latlng.toString())
        .openPopup();

        document.getElementById("lat").value = e.latlng.lat;
        document.getElementById("lng").value = e.latlng.lng;
}
map.on('click', onMapClick);
    
        
