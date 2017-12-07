
/////////////////////////
// HOMEPAGE FADE IMAGE //
/////////////////////////

$('#login-route').hide();

$('#home-img, .gallery-text, #login-route').hover(
    function() {
        $('#darkness').fadeTo(50, 1);
        $("#home-img").css("-webkit-filter", "brightness(200%)");
        $('#login-route').show();
    },
    function(evt){
        if (evt.toElement === $('#darkness')[0]) {
            $('#darkness').fadeTo(50, 0);
            $("#home-img").css("-webkit-filter", "brightness(100%)");
            $('#login-route').hide();
        }
    }
);

// $('#home-img, .gallery-text, #login-route').hover(
//     function() {
//         $('#darkness').fadeTo(25, 1);
//         $("#home-img").css("-webkit-filter", "brightness(200%)");
//     },
//     function(){
//         $('#darkness').fadeTo(25, 0,
//             function(){
//                 $(this).show();
//             }
//         );
//         $("#home-img").css("-webkit-filter", "brightness(100%)");
//     }
// );

// USAGE


// $('#home-img').hover(function(){
//     $('#login-route').show();
// });

