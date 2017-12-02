

// $('[data-js="btn"]').hover(function(){
//   $(this).toggleClass('active');
//   if ($(this).hasClass('active')) {
//     $('body').addClass('blur');
//   } else {
//     $('body').removeClass('blur');
//   }
// });

// $('#home-img').hover(function(){
//     $('#login-route').fadeTo(200, 1);
// }, function(){
//     $('#login-route').fadeTo(200, 0, function(){
//         $("#login-route").hide();
//     });
// });

// $('#home-img').hover(function(){
//     $('#darkness').fadeTo(200, 1);
// }, function(){

//     $('#darkness').fadeTo(200, 0, function(){
//         $(this).hide();
//     });
// });

// $('#home-img').hover(function(){
//     $('#darkness').fadeTo(200, 1);
// });

$('#home-img').hover(function(){
    $('#darkness').fadeTo(200, 1);
}, function(){
    $('#darkness').fadeTo(200, 0, function(){
        $(this).hide();
    });
});