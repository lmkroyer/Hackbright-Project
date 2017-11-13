
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
  // let geocoder = new google.maps.Geocoder();
};


// function addGeocode() {
//   let geocoder = new google.maps.Geocoder();
//   let mapOptions = {

//   }
// }

////////////
// geocode //
////////////

// TODO: put id on the things!

// function codeActiveCases() {
//     let address = document.getElementById('XYZ').value;
//     geocoder.geocode( { 'XYZ': XYZ}, function(results, status) {
//       if (status == 'OK') {
//         map.setCenter(unitedStates);
//         let marker = new google.maps.Marker({
//             map: map,
//             position: results[0].geometry.location
//               // icon: {
//               //   path: google.maps.SymbolPath.CIRCLE,
//               //   scale: 10,
//               //   fillColor: 'red'
//               // },
//         });
//       } else {
//         alert('Geocode was not successful for the following reason: ' + status);
//       }
//     });
//   }

////////////
// marker //
////////////

// FIXME: Add each case here -- fix where to put on map, link to db:

// $.get('/active_cases.json', function(activeCases) {

//   let activeCase, marker;

//   for (let key in cases) {
//     activeCase = cases[key];

//     marker = new google.maps.Marker({
//         position: new google.maps.LatLng(activeCase.caseCounty, activeCase.caseState),
//         map: map,
//         title: 'Case ID: ' + activeCase.caseId,
//         icon: {
//           path: google.maps.SymbolPath.CIRCLE,
//           scale: 10,
//           fillColor: 'red'
//         },
//     });
//   }
// }

// function addMarker() {
//   let marker = new google.maps.Marker({
//      position: new google.maps.LatLng(XYZ),
//       icon: {
//         path: google.maps.SymbolPath.CIRCLE,
//         scale: 10,
//         fillColor: 'red'
//       },
//       map: map
//   });
//   return marker;
// }

// let marker = addMarker();

google.maps.event.addDomListener(window, 'load', initMap);