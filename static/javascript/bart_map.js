

let streetmap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

// Initialize all the LayerGroups that we'll use.
let layers = {
  TRANSFER: new L.LayerGroup(),
  BLUE: new L.LayerGroup(),
  GREEN: new L.LayerGroup(),
  ORANGE: new L.LayerGroup(),
  RED: new L.LayerGroup(),
  YELLOW: new L.LayerGroup()
};
// Create the map with our layers.
let map = L.map("map", {
  center: [37.7749, -122.4194],
  zoom: 10,
  layers: [
    layers.TRANSFER,
    layers.BLUE,
    layers.GREEN,
    layers.ORANGE,
    layers.RED,
    layers.YELLOW,
  ]
});

window.BartStationMap = map;

// Add our "streetmap" tile layer to the map.
streetmap.addTo(map);
// Create an overlays object to add to the layer control.
let overlays = {
  "Transfer Station": layers.TRANSFER,
  "Blue Line": layers.BLUE,
  "Green Line": layers.GREEN,
  "Orange Line": layers.ORANGE,
  "Red Line": layers.RED,
  "Yellow Line": layers.YELLOW
};
// Create a control for our layers, and add our overlays to it.
L.control.layers(null, overlays).addTo(map);

// Create a legend to display information about our map.
let info = L.control({
  position: "topright"
});
// When the layer control is added, insert a div with the class of "legend".
info.onAdd = function () {
  let div = L.DomUtil.create("div", "legend");
  return div;
};
// Add the info legend to the map.
info.addTo(map);
// Initialize an object that contains icons for each layer group.
let icons = {
  TRANSFER: L.ExtraMarkers.icon({
    icon: "ion-android-train",
    iconColor: "white",
    markerColor: "black",
    shape: "circle"
  }),
  BLUE: L.ExtraMarkers.icon({
    icon: "ion-android-train",
    iconColor: "black",
    markerColor: "blue",
    shape: "circle"
  }),
  GREEN: L.ExtraMarkers.icon({
    icon: "ion-android-train",
    iconColor: "black",
    markerColor: "green",
    shape: "circle"
  }),
  ORANGE: L.ExtraMarkers.icon({
    icon: "ion-android-train",
    iconColor: "black",
    markerColor: "orange",
    shape: "circle"
  }),
  RED: L.ExtraMarkers.icon({
    icon: "ion-android-train",
    iconColor: "black",
    markerColor: "red",
    shape: "circle"
  }),
  YELLOW: L.ExtraMarkers.icon({
    icon: "ion-android-train",
    iconColor: "black",
    markerColor: "yellow",
    shape: "circle"
  })
};
d3.json('https://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V&json=y').then(function (stationInfo) {
  d3.json('https://api.bart.gov/api/route.aspx?cmd=routeinfo&route=all&key=MW9S-E7SL-26DU-VV8V&json=y').then(function (routeInfo) {
    let stationLocation = stationInfo['root']['stations']['station'];
    let route = routeInfo['root']['routes']['route'];

    // Create an object to keep the number of markers in each layer.
    let stationCount = {
      TRANSFER: 0,
      BLUE: 0,
      GREEN: 0,
      ORANGE: 0,
      RED: 0,
      YELLOW: 0
    };


    // create list of stations for each color of line 
    // const stations = [blueLineStations,greenLineStations, orangeLineStations, redLineStations,yellowLineStations]
    var blueLineStations = route.filter(function (blue) {
      return blue['number'] == '12'
    }).map(function (blue) {
      return blue['config']['station']
    })[0]

    var greenLineStations = route.filter(function (green) {
      return green['number'] == '6'
    }).map(function (green) {
      return green['config']['station']
    })[0];

    var orangeLineStations = route.filter(function (orange) {
      return orange['number'] == '4'
    }).map(function (orange) {
      return orange['config']['station']
    })[0];

    var redLineStations = route.filter(function (red) {
      return red['number'] == '8'
    }).map(function (red) {
      return red['config']['station']
    })[0];

    var yellowLineStations = route.filter(function (yellow) {
      return yellow['number'] == '2'
    }).map(function (yellow) {
      return yellow['config']['station']
    })[0];

    // create a list where it adds station abbr to a list and then have a another list where if the abbr appears more than once it adds it to that one for tramsfer stations
    var stationAbbr = [];


    blueLineStations.forEach(function (station) {
      stationAbbr.push(station);
    });
    greenLineStations.forEach(function (station) {
      stationAbbr.push(station);
    });
    orangeLineStations.forEach(function (station) {
      stationAbbr.push(station);
    });
    redLineStations.forEach(function (station) {
      stationAbbr.push(station);
    });
    yellowLineStations.forEach(function (station) {
      stationAbbr.push(station);
    });

    console.log(stationAbbr)



    //create a list for tansfer stations
    var transferStation = []


    // create function to compare lists
    function compareList(list1, list2) {
      new Set(list1).forEach(function (item) {
        if (list2.includes(item) && !transferStation.includes(item)) {
          transferStation.push(item)
        }
      })
    }
    compareList(blueLineStations, greenLineStations)
    compareList(blueLineStations, orangeLineStations)
    compareList(blueLineStations, redLineStations)
    compareList(blueLineStations, yellowLineStations)
    compareList(greenLineStations, orangeLineStations)
    compareList(greenLineStations, redLineStations)
    compareList(greenLineStations, yellowLineStations)
    compareList(orangeLineStations, redLineStations)
    compareList(orangeLineStations, yellowLineStations)
    compareList(redLineStations, yellowLineStations)


    console.log(transferStation)


    // Initialize stationStatusCode, which will be used as a key to access the appropriate layers, icons, and station count for the layer group.
    let stationColorCode;


    stationLocation.forEach(function (station) {
      // Determine the line based on the station abbreviation from station.config.station
      if (transferStation.includes(station['abbr'])) {
        stationColorCode = "TRANSFER";
      } else if (blueLineStations.includes(station['abbr'])) {
        stationColorCode = "BLUE";
      } else if (greenLineStations.includes(station['abbr'])) {
        stationColorCode = "GREEN";
      } else if (orangeLineStations.includes(station['abbr'])) {
        stationColorCode = "ORANGE";
      } else if (redLineStations.includes(station['abbr'])) {
        stationColorCode = "RED";
      } else if (yellowLineStations.includes(station['abbr'])) {
        stationColorCode = "YELLOW";
      } else {
        return; // Skip stations that are not in any defined line
      }



      // Update the station count
      stationCount[stationColorCode]++;

      // Create a new marker with the appropriate icon and add it to the corresponding layer group
      let newMarker = L.marker([station['gtfs_latitude'], station['gtfs_longitude']], {
        icon: icons[stationColorCode]
      });

      // Add the new marker to the layer group
      newMarker.addTo(layers[stationColorCode]);


      // Optionally bind a popup to the marker with more information
      newMarker.bindPopup(`<h3>${station['name']}</h3><p>Station Address: ${station['address']}</p><p>Route Color: ${stationColorCode}</p>`);
      // Zoom the map to the station location when the station is selected
      newMarker.on('click', function () {
        map.setView([station['gtfs_latitude'], station['gtfs_longitude']], 14);
      });




    });



    console.log(stationCount)

  });
});