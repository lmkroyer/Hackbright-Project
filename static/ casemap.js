
// HOMEPAGE MAP

"use strict";

function initMap() {

  // Specify where the map is centered
  // Defining this variable outside of the map options makes
  // it easier to dynamically change if you need to recenter
  let unitedStates = {lat: 39, lng: -95};

  // Create a map object and specify the DOM element for display.
  let map = new google.maps.Map(document.querySelector('#map'), {
    center: unitedStates,
    mapTypeControl: false,
    scrollwheel: false,
    zoom: 1,
    zoomControl: false,
    streetViewControl: false,
    styles: MAPSTYLES,
    mapTypeId: google.maps.MapTypeId.ROADMAP
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