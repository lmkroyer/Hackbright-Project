
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

$("#show-timeline").click(function(){
    $("#timeline").toggle();
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

///////////////////
// SEARCH ENGINE //
///////////////////

// function getSearchEntry() {

//     let search = document.getElementById('search-engine');
//     $.get("/searchResults.json", function (data) {
//         // put search result display here
//                                 });


/////////////////////
// MAKE A TIMELINE //
/////////////////////

// class Timeline {

//     constructor(displayElement){

//         displayElement.append(`<img id="image">
//                               <h1 id="title"></h1>
//                               <p id="date"></p>
//                               <p id="start"></p>
//                               <p id="end"></p>
//                               <p id="location"> </p>
//                               <p id="description"></p>`);

//         // Set properties on the class
//         this.container = displayElement;
//         this.imageEl = displayElement.children("img#image");
//         this.titleEl = displayElement.children("h1#title");
//         this.dateEl = displayElement.children("p#date");
//         this.startEl = displayElement.children("p#start");
//         this.endEl = displayElement.children("p#end");
//         this.locationEl = displayElement.children("p#location");
//         this.descriptionEl = displayElement.children("p#description");

//     }

//     changeTimeline(my_case){
//         this.titleEl.text(my_case);
//     }

//     changeDate(newDate) {
//         this.dateEl.text("Join us on " + newDate);
//     }

//     changeStart(newStart) {
//         this.startEl.text(newStart);
//     }

//     changeEnd(newEnd) {
//         this.endEl.text(newEnd);
//     }

//     changeImage(newImage){
//         this.imageEl.attr("src", newImage);
//     }

//     changeFont(newFont) {
//         this.container.css("font-family", newFont);
//     }

//     changeLocation(newLocation) {
//         this.locationEl.text(newLocation);
//     }

//     changeDescription(newDescription) {
//         this.descriptionEl.text(newDescription);
//     }

//     changeBackgroundColor(newBackgroundColor) {
//         this.container.css("background-color", newBackgroundColor);
//     }

// }


// PART 2:

// Create your invitation object
// let invitationElement = $("#invite-display");
// let invite = new Invitation(invitationElement);

// // Add event listeners
// $('#show-timeline').on('click', function (evt) {
//     //or could do evt.target.value
//     invite.changeTimeline($('#title-input').val());
// });

// $('#date-input').on('change', function (evt) {
//     invite.changeDate($('#date-input').val());
// });

// $('#start-time').on('change', function (evt) {
//     invite.changeStart($('#start-time').val());
// });

// $('#end-time').on('change', function (evt) {
//     invite.changeEnd($('#end-time').val());
// });

// $('#location-input').on('change', function (evt) {
//     invite.changeLocation($('#location-input').val());
// });

// $('#description-input').on('change', function (evt) {
//     invite.changeDescription($('#description-input').val());
// });

// $('#font').on('change', function (evt) {
//     invite.changeFont($('#font').val());
// });

// $(".color-btn").on('click', function (evt) {
//     invite.changeBackgroundColor($(evt.target).data("color"));
// });

// $(".image-input").on('click', function (evt) {
//     invite.changeImage(evt.target.value);
// })
