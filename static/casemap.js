
// HOMEPAGE MAP

"use strict";

// or try 39.8097343, -98.5556199)
// let unitedStates = {lat: 39, lng: -95};

// let map = new google.maps.Map(document.querySelector('#map'), {
//     center: unitedStates,
//     zoom: 3,
//     mapTypeControl: false,
//     zoomControl: false,
//     scaleControl: true,
//     streetViewControl: false,

// });

function initMap() {

  // Specify where the map is centered
  // Defining this variable outside of the map options makes
  // it easier to dynamically change if you need to recenter
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

// TODO: Add each case here:

// function addMarker() {
//   let myImageURL = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
//   let nearSydney = new google.maps.LatLng(-34.788666, 150.41146);
//   let marker = new google.maps.Marker({
//       position: nearSydney,
//       map: map,
//       title: 'Hover text',
//       icon: myImageURL
//   });
//   return marker;
// }

// let marker = addMarker();

google.maps.event.addDomListener(window, 'load', initMap);