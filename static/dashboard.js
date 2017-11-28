
"use strict";

// function getCaseStatus() {

//     let status = document.getElementById('caseID');

//     let cases = document.getElementById('caseList');

//     for (let cse of cases) {

//         if (cse.request_pro_docs.submitted) {
//             return '100%';
//         }
//         else if (cse.interrogatories.submitted) {
//             return '75%';
//         }
//         else if (cse.answer.submitted) {
//             return '50%';
//         }
//         else if (cse.complaint.processed) {
//             return '25%';
//         }
//         else {
//             return '0%';
//         }
// FIXME: this needs to show status!


// let caseStatus = document.querySelector("#case-status");
// caseStatus.innerHTML = getCaseStatus();

// function insertText() {
//     document.getElementById('td1').innerHTML = "Some text to enter";
// }

///////////////////////////////
// ATTNY BAR CHART FUNCTIONS //
///////////////////////////////

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


// function showTimeline(case_id) {
//     $.get("/caseTimeline.json", function (data) {
//       let myLineChart = Chart.Line(ctx_line, {
//                                     data: data,
//                                     options: options
//                                 });
//       // $("#lineLegend").html(myLineChart.generateLegend());
//     });
// }

$("#availChart").click(function(){
    createAttnyAvail();
    $("#attnyBarChart").toggle();
    $("#progressChart").toggle();
});

$("#expandRow").click(function(){
    $("#collapsedRow").toggle();
});

//////////////////////////////////
// USER LINE GRAPH ON DASHBOARD //
//////////////////////////////////

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

///////////////////////
// NOTEPAD FUNCTIONS //
///////////////////////

function checkWebStorageSupport() {
    if(typeof(Storage) !== "undefined") {
        return(true);
    }
    else {
        alert("Web storage unsupported!");
        return(false);
    }
}

function displaySavedNote() {

    if(checkWebStorageSupport() == true) {
        result = localStorage.getItem('note');
    }

    if(result === null) {
        result = "No note saved";
    }
    document.getElementById('area').value = result;
}

function listSavedNotes(caseID) {

    if(checkWebStorageSupport() == true) {

        let noteValues = [],
        noteKeys = Object.keys(localStorage),
        i = noteKeys.length;

        while ( i-- ) {
            noteValues.push( localStorage.getItem(noteKeys[i]) );
        }

        let specCaseNotes = [];

        // FIXME: here is psuedocode
        // for item in noteValues:
        //     JSON.parse(item)
        //     if item.case_id == caseID:
        //         specCaseNotes.append(item)

        //         document.getElementById('saved-ntoes').value = item;
                $('#saved-notes').html(item.key);



        // result = localStorage.getItem('note');
    }

    if(result === null) {
        result = "No note saved";
    }

    document.getElementById('area').value = result;
}

function saveNote(caseID) {

    let today = new Date();
    let todayStr = today.toDateString();

    if(checkWebStorageSupport() == true) {
        let noteInput = document.getElementById("area");

        if(noteInput.value != '') {

            let noteObj = {'case_id':caseID,
                           'text': noteInput.value,
                           'date': todayStr
                          };

            let noteObjJSON = JSON.stringify(noteObj);
            let noteName = "Note" + noteObj.date;

            localStorage.setItem(noteName, noteObjJSON);
        }
        else {
            alert("Nothing to save");
        }
    }
}

function downloadNote(filename) {
    let text = document.getElementById("area");
    let pom = document.createElement('a');
    pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    pom.setAttribute('download', filename);

    if (document.createEvent) {
        let event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function closeNote() {
    // this line clears content
    // document.getElementById('area').value = "";
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
}


$("#new-note").click(function(){
    let caseID = $(this).data("case-id");
    $("#save-note").data("case-id", caseID);
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
});


$("#close-note").click(function(){
    closeNote(caseID);
});


$("#save-note").click(function(){
    let caseID = $(this).data("case-id");
    console.log(caseID);
    saveNote(caseID);
});


$("#download-note").click(function(){
    downloadNote();
});


// $("#div"+case.case_id).click(function() {

// }

// JSON.stringify() --> returns a string (from an object)
// JSON.parse() --> turns strings back into object


///////////////////
// SEARCH ENGINE //
///////////////////


$("#lit-search").click(function() {

    let search = $('#user-lit-search');

    $.get("/search_results/" + search.val(), function (data) {

        // this is a list of documents
        // let results = data;

        // for (let result of results) {
        let resultsContent = "<table>";

        for (i=0; i < 100; i++) {
            resultsContent += '<tr><td>' + 'result ' +  i + ':' + result + '</td></tr>';
        }

        resultsContent += "</table>";

        $('#search-results-table').append(resultsContent);

    });



    $("#search-results-table").toggle();
    $("#progressChart").toggle();
    $("#caseInfo").toggle();
});



/////////////////////
// MAKE A TIMELINE //
/////////////////////

// function caseHistory() {

//     $.get("/casehistory.json");
// }

// let CASEHISTORY = caseHistory();

function showCaseHistory(buttonID) {

    $.get("/casehistory.json", function (data) {
        $('#complaint-info').html(data[buttonID]['complaint']);
        $('#answer-info').html(data[buttonID]['answer']);
    });
}


$(".show-timeline").click(function(){
    $("#timeline").toggle();
    $("#progressChart").toggle();
    let buttonID = $(this).attr("id");
    showCaseHistory(buttonID);
});


// preload all the cases into the DOM
// server side: format into in json

// global variable (js): json object of all cases (case_id: {attribute1: attribute1
//                                                             })

// map each id to button

// inside event listener callback: use this or evt.target

// 1. write html jinja look that
// 2. each box on timeline gets ID that matches attribute names from data dict
// jquery element from complaint div

// attach event listener to class of buttons, each button will store case ID, so function with
//     event listener will call the specific case info in the data dict (using this.attr('id'))

//     {case 1: {complaint: attribute,
//               answer: attribute,
//               interrogatories: attribute,
//     case 2: {complaintL attribute

//         ...}}}

// (".class").on click - event function

// start with html data attributes, make server data dict, write js functions that listen for id and populate jinja loop

