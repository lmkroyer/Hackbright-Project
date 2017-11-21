
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
    $("#startingChart").toggle();
});


$("#expandRow").click(function(){
    $("#collapsedRow").toggle();
});


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
        var area = document.getElementById("area");
        if(area.value != '') {
            localStorage.setItem("note", area.value);
        }
        else {
            alert("Nothing to save");
        }
    }
}

function clear() {
    document.getElementById('area').value = "";
}

$("#newNote").click(function(){
    $("#notepad").toggle();
    $("#notepadControls").toggle();
    $("#startingChart").toggle();
});