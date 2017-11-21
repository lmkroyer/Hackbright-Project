
// HOMEPAGE MAP

"use strict";

function initMap() {

  // Specify where the map is centered
  let unitedStates = {lat: 39, lng: -95};

  // Create a map object and specify the DOM element for display.
  let map = new google.maps.Map(document.querySelector('#map'), {
    center: unitedStates,
    scrollwheel: false,
    zoom: 4,
    zoomControl: true,
    streetViewControl: false,
    styles: MAPSTYLES,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });


// ////////////
// // marker //
// ////////////


  $.get('/active_cases.json', function(activeCases) {

    for (let key in activeCases) {
         let activeCaseCounty = activeCases[key]['caseCounty'];

      let geocode_generator = new google.maps.Geocoder();
      let administrative_area_level_2 =  activeCaseCounty + ' County';

      geocode_generator.geocode({'address': administrative_area_level_2}, function(results, status) {
          if (status === google.maps.GeocoderStatus.OK) {
            map.setCenter(unitedStates);

            let marker = new google.maps.Marker({
              map: map,
              place: {
                location: results[0].geometry.location,
                query: "Case ID"
              },
              icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 10,
                fillColor: '#ff0000',
                fillOpacity: 1,
                strokeColor: '',
                // strokeWeight: 0
              }
            });
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
      });
    }
  });

}
