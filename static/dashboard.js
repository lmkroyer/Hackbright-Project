
"use strict";

//////////////////////////////
// CASE TABLE - CASE STATUS //
//////////////////////////////

function getCaseStatus() {

    let myCase = document.getElementById('case-status');

    console.log(myCase);
    let myCaseObj= $(myCase).data("case");

    console.log(myCaseObj);

    // let cases = document.getElementById('caseList');

    // for (let cse of cases) {

    if (myCaseObj.request_pro_docs && myCaseObj.request_pro_docs.date_submitted) {
        let status = '100%';
    }
    else if (myCaseObj.interrogatories && myCaseObj.interrogatories.date_submitted) {
        let status = '75%';
    }
    else if (myCaseObj.answer && myCaseObj.answer.date_submitted) {
        let status = '50%';
    }
    else if (myCaseObj.complaint && myCaseObj.complaint.date_processed) {
        let status = '25%';
    }
    else {
        let status = '0%';
    }

    console.log(status);
    // document.getElementById('case-status').innerHTML = status;

    // $("#case-status").html(status);
}

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

// $("#expandRow").click(function(){
//     $("#collapsedRow").toggle();
// });

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

function displaySavedNote(noteKey) {

    if(checkWebStorageSupport() === true) {
        let result = JSON.parse(localStorage.getItem(noteKey));

        if (result === null) {
        result = "No note saved";
        }

        document.getElementById('area').value = result.txt;
    }
}

function listSavedNotes(caseID) {

    if(checkWebStorageSupport() === true) {

        let noteValues = {},
        noteKeys = Object.keys(localStorage);

        for (let key of noteKeys) {
            let noteObj = JSON.parse(localStorage.getItem(key));
            if (noteObj.case_id == caseID) {
                noteValues[key] = noteObj;
            }
        }
        // i = noteKeys.length;
        // while ( i-- ) {
        //     console.log(noteKeys);
        //     let noteObj = JSON.parse(localStorage.getItem(noteKeys[i]));
        //     if (noteObj.case_id == caseID) {
        //         noteValues.push(noteObj);
        //     }
        // }
        console.log(noteValues);

        let trHTML = '';

        for (let key in noteValues) {
            let value = noteValues[key];
            trHTML += "<tr><td><li><a href='#' class='case-note' data-key='" + key + "'>" + "Note: " + value.date + "</a></li></td></tr>";
        }
        // $.each(noteValues, function(j, item) {
        //     console.log(item);
        //     trHTML += "<tr><td><li><a href='#' class='case-note' data-object='" + item + "'>" + "Note: " + item.date + "</a></li></td></tr>";
        // });

        $("#display-notes").html("<b>Notes:</b>");
        $("#display-notes").append(trHTML);
    }
}

function saveNote(caseID) {

    let today = new Date();
    let todayStr = today.toDateString();
    let todayStrKey = String(today);

    if(checkWebStorageSupport() == true) {
        let noteInput = document.getElementById("area");

        if(noteInput.value != '') {

            let noteObj = {"case_id":caseID,
                           "txt": noteInput.value,
                           "date": todayStr
                          };

            let noteObjJSON = JSON.stringify(noteObj);
            localStorage.setItem(todayStrKey, noteObjJSON);
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
    document.getElementById('area').value = "";
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
}


$("#new-notes").click(function(){
    document.getElementById('area').value = "";
    let caseID = $(this).data("case-id");
    $("#save-note").attr("data-case-id", caseID);
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
});

$("#close-note").click(function(){
    closeNote();
});


$("#save-note").click(function(){
    let caseID = $(this).data("case-id");
    saveNote(caseID);
});


$("#download-note").click(function(){
    downloadNote();
});

$("#case-row").click(function(){
    let caseID = $(this).data("case-id");
    listSavedNotes(caseID);
});

$(document).on("click", ".case-note", function(){
    let noteKey = $(this).data("key");
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#progressChart").toggle();
    displaySavedNote(noteKey);
});


// $("#div"+case.case_id).click(function() {

// }

// JSON.stringify() --> returns a string (from an object)



///////////////////
// SEARCH ENGINE //
///////////////////


function getResults() {

    let query = $("#user-lit-search").val();

    $.get("/search_results/" + query, function(data) {

        console.log(data);

        let trHTML = '';

        for (let result in data) {

            let previewText = data[result].highlights;
            let path = data[result].path;

            console.log(path);
            // let previewText = result['highlights'];
            trHTML += "<tr><td>" + previewText + "</td></tr>";
            trHTML += "<tr><td><a href='/download/" + path + "'>Download</a></td></tr>";
        }

    // below worked to display path
        // $.each(data, function(i, item) {
        //     trHTML += "<tr><td>" + item + "</td></tr>";

        //     console.log(typeof(item));

        // });

        $("#search-results-table").append(trHTML);

    });

    $("#search-results-table").toggle();
    $("#search-results-div").toggle();
    $("#progressChart").toggle();
    $("#caseInfo").toggle();
}

$("#user-lit-search").keyup(function(event) {
    // if person pressed enter
    if (event.which == 13) {
        getResults();
    }
    });

$("#lit-search").click(function(event) {
    getResults();
    });

$("#dash-redirect").click(function() {
    $("#search-results-table").toggle();
    $("#search-results-div").toggle();
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



////////////////////
// BOUNDING BOXES //
////////////////////

$("#bounding-box-btn").click(function(){
    $("#caseInfo").toggle();
    $("#progressChart").toggle();
});



