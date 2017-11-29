function createAttnyAvail() {

    let options = {
        responsive: true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }

    let ctx_bar = $("#attnyBarChart").get(0).getContext("2d");

    // let green_red_gradient = bar_ctx.createLinearGradient(0, 0, 0, 600);
    // green_red_gradient.addColorStop(0, 'red');
    // green_red_gradient.addColorStop(1, 'green');

    $.get("/attorney_data.json", function (data) {
      let attorneyAvail = new Chart(ctx_bar, {
                                              type: 'horizontalBar',
                                              data: data,
                                              options: options
                                            });
    });

}

$('.tree-toggle').click(function () {
    $(this).parent().children('ul.tree').toggle(200);
});

$("document").ready(function() {
$("#formFund").click(function(){
    $("#allOptions").hide();
    $("#LPA-generator").show();
});
})

// $("#sum-{{ fund.fund }}").click(function(){
//     $("#allOptions").toggle();
//     // $("#LPA-generator").toggle();
//     $("#sum-rep").toggle();
// });


$("#availChart").click(function(){
    createAttnyAvail();
    $("#attnyBarChart").toggle();
    $("#allOptions").toggle();
});

// $("document").ready(function() {
// $("#start-sum-rep").click(function(){
//     $("#allOptions").hide();
//     $("#upload-sum-rep").show();
// });
// });

$("#start-sum-rep").click(function(){
    $("#upload-sum-rep").toggle();
    $("#allOptions").toggle();
});