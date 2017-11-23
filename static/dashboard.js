
"use strict";

function getCaseStatus() {

    let status = document.getElementById('caseID');

    let cases = document.getElementById('caseList');

    for (let cse of cases) {

        if (cse.request_pro_docs.submitted) {
            return '100%';
        }
        else if (cse.interrogatories.submitted) {
            return '75%';
        }
        else if (cse.answer.submitted) {
            return '50%';
        }
        else if (cse.complaint.processed) {
            return '25%';
        }
        else {
            return '0%';
        }
// FIXME: this needs to show status!


let caseStatus = document.querySelector("#case-status");
caseStatus.innerHTML = getCaseStatus();

function insertText () {
    document.getElementById('td1').innerHTML = "Some text to enter";
}


// ATTNY BAR CHART FUNCTIONS

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

$("#availChart").click(function(){
    createAttnyAvail();
    $("#attnyBarChart").toggle();
    $("#progressChart").toggle();
});


$("#expandRow").click(function(){
    $("#collapsedRow").toggle();
});


// USER LINE GRAPH ON DASHBOARD

function showUserInfo() {

    // Make Line Chart of Melon Sales over time
    let ctx_line = $("#progressChart").get(0).getContext("2d");

    let options = {
      responsive: true
    };

    $.get("/userProgress.json", function (data) {
      let myLineChart = Chart.Line(ctx_line, {
                                    data: data,
                                    options: options
                                });
      // $("#lineLegend").html(myLineChart.generateLegend());
    });
}

showUserInfo();


// START A NEW CASE


// $("#caseInit").click(function(){
//     $("#progressChart").toggle();
// });


// NOTEPAD FUNCTIONS

function check_web_storage_support() {
    if(typeof(Storage) !== "undefined") {
        return(true);
    }
    else {
        alert("Web storage unsupported!");
        return(false);
    }
}

function display_saved_note() {
    if(check_web_storage_support() == true) {
        result = localStorage.getItem('note');
    }
    if(result === null) {
        result = "No note saved";
    }
    document.getElementById('area').value = result;
}

function save() {
    if(check_web_storage_support() == true) {
        let area = document.getElementById("area");
        if(area.value != '') {
            localStorage.setItem("note", area.value);
        }
        else {
            alert("Nothing to save");
        }
    }
}

// function download(filename) {
//     let text = document.getElementById("area");
//     let pom = document.createElement('a');
//     pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
//     pom.setAttribute('download', filename);

//     if (document.createEvent) {
//         let event = document.createEvent('MouseEvents');
//         event.initEvent('click', true, true);
//         pom.dispatchEvent(event);
//     }
//     else {
//         pom.click();
//     }
// }

function close() {
    // this line clears content
    // document.getElementById('area').value = "";
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
}

$("#newNote").click(function(){
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
});