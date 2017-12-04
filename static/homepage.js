
/////////////////////////
// HOMEPAGE FADE IMAGE //
/////////////////////////

$('#home-img').hover(function(){
    $('#darkness').fadeTo(25, 1);
}, function(){
    $('#darkness').fadeTo(25, 0, function(){
        $(this).show();
        $('#login-route').hide();
    });
});

// USAGE
$('#login-route').hide();

$('#home-img').hover(function(){
    $('#login-route').show();
});

