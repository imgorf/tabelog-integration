let map;
async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    map = new Map(document.getElementById("map"), {
    center: { lat: 1.352, lng: 103.820 },
    zoom: 10,
    mapId: 'e0a0a647cdc72aae'
    });
}

initMap();