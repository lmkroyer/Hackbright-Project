
// HOMEPAGE MAP

"use strict";

function initMap() {

  // Specify where the map is centered
  let unitedStates = {lat: 39, lng: -95};

  // Create a map object and specify the DOM element for display.
  let map = new google.maps.Map(document.querySelector('#map'), {
    center: unitedStates,
    scrollwheel: false,
    zoom: 5,
    zoomControl: true,
    streetViewControl: false,
    styles: MAPSTYLES,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });
  // let geocoder = new google.maps.Geocoder();



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
//   //   let address = document.getElementById('XYZ').value;
//   //   geocoder.geocode( { 'XYZ': XYZ}, function(results, status) {
//   //     if (status == 'OK') {
//   //       map.setCenter(unitedStates);
//   //       let marker = new google.maps.Marker({
//   //           map: map,
//   //           position: results[0].geometry.location
//   //             // icon: {
//   //             //   path: google.maps.SymbolPath.CIRCLE,
//   //             //   scale: 10,
//   //             //   fillColor: 'red'
//   //             // },
//   //       });
//   //     } else {
//   //       alert('Geocode was not successful for the following reason: ' + status);
//   //     }
//   //   });
//   // }

// ////////////
// // marker //
// ////////////

// FIXME: pull in custom marker icon above, plus pass unitedStates to map.setCenter

  $.get('/active_cases.json', function(activeCases) {

    console.log(activeCases);

    for (let key in activeCases) {
         let activeCaseCounty = activeCases[key]['caseCounty'];

      let geocode_generator = new google.maps.Geocoder();
      let administrative_area_level_2 =  activeCaseCounty + ' County';

      geocode_generator.geocode({'address': administrative_area_level_2}, function(results, status) {
          if (status === google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);

            let marker = new google.maps.Marker({
              map: map,
              place: {
                location: results[0].geometry.location,
                query: "Case ID"
              }
            });
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
      });
    }
  });

}
