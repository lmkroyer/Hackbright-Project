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

//////////////////////////
// SUMMARY REPORT TABLE //
//////////////////////////

// Model:
// function showCaseHistory(buttonID) {

//     $.get("/casehistory.json", function (data) {
//         $('#complaint-info').html(data[buttonID]['complaint']);
//         $('#answer-info').html(data[buttonID]['answer']);
//     });
// }

function buildSummaryReport(clientID) {

    $.get('/summaryreport/' + clientID, function (data) {





}


$("#start-sum-rep").click(function(){
    $("#upload-sum-rep").toggle();
    $("#allOptions").toggle();
});

$(".show-sum-rep").click(function(){
    $("#allOptions").toggle();
    // $("#LPA-generator").toggle();
    $("#sum-rep").toggle();
    let clientID = $(this).attr("id");
    buildSummaryReport(clientID);
});

