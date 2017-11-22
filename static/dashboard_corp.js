$('.tree-toggle').click(function () {
    $(this).parent().children('ul.tree').toggle(200);
});


$("document").ready(function() {
$("#formFund").click(function(){
    $("#allOptions").hide();
    $("#LPA-generator").show();
});
})