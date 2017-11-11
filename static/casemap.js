
// HOMEPAGE MAP

"use strict";

function initMap() {

  // Specify where the map is centered
  let unitedStates = {lat: 39, lng: -95};

  // Create a map object and specify the DOM element for display.
  let map = new google.maps.Map(document.querySelector('#map'), {
    center: unitedStates,
    scrollwheel: false,
    zoom: 3,
    zoomControl: true,
    streetViewControl: false,
    styles: MAPSTYLES,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });

};

////////////
// marker //
////////////

// FIXME: Add each case here -- fix where to put on map, link to db:

function addMarker() {
  let markerLocation = map.getCenter();
  let marker = new google.maps.Marker({
     position: new google.maps.LatLng(XYZ),
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 10,
        fillColor: 'red'
      },
      map: map
  });
  return marker;
}

let marker = addMarker();

google.maps.event.addDomListener(window, 'load', initMap);