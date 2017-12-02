
/////////////////////////
// HOMEPAGE FADE IMAGE //
/////////////////////////

$('#home-img').hover(function(){
    $('#darkness').fadeTo(25, 1);
}, function(){
    $('#darkness').fadeTo(25, 0, function(){
        $(this).show();
        // $('#login-route').show();
    });
});

// ;(function($) {

// $.fn.letterDrop = function() {
//   // Chainability
//   return this.each( function() {

//   let obj = $( this );

//   let drop = {
//     arr : obj.text().split( '' ),

//     range : {
//       min : 1,
//       max : 9
//     },

//     styles : function() {
//       let dropDelays = '\n', addCSS;

//        for ( i = this.range.min; i <= this.range.max; i++ ) {
//          dropDelays += '.ld' + i + ' { animation-delay: 1.' + i + 's; }\n';
//        }

//         addCSS = $( '<style>' + dropDelays + '</style>' );
//         $( 'head' ).append( addCSS );
//     },

//     main : function() {
//       let dp = 0;
//       obj.text( '' );

//       $.each( this.arr, function( index, value ) {

//         dp = dp.randomInt( drop.range.min, drop.range.max );

//         if ( value === ' ' )
//           value = '&nbsp';

//           obj.append( '<span class="letterDrop ld' + dp + '">' + value + '</span>' );

//       });

//     }
//   };

//   Number.prototype.randomInt = function ( min, max ) {
//     return Math.floor( Math.random() * ( max - min + 1 ) + min );
//   };


//   // Create styles
//   drop.styles();


//     // Initialise
//     drop.main();
//   });

// };

// }(jQuery));


// USAGE
$('#login-route').hide();

$('#home-img').hover(function(){
    $('#login-route').show();
    $( '#login-route' ).letterDrop();
});

// $( '#greet-user' ).letterDrop();



// $('#home-img').hover(function(){
//     $('#home-img').fadeTo(200, 0.1);
// }, function(){
//     $('#home-img').fadeTo(200, 1, function(){
//         $(this).show();
//     });
// });

// below makes both image and screen dark
// $('#home-img').hover(function(){
//     $('#darkness').fadeTo(200, 1);
// }, function(){
//     $('#darkness').fadeTo(200, 0, function(){
//         $(this).show();
//         $('#login-route').show();
//     });
// });

// $('#home-img').hover(function(){
//     $('#home-img').fadeTo(200, 0.1);
// }, function(){
//     $('#home-img').fadeTo(200, 1, function(){
//         $(this).show();
//     });
// });