window.csrftoken="{{csrftoken}}";
<<<<<<< HEAD
//window.onload = clock();
=======
window.onload = clock();
/*
>>>>>>> 2390f1179d452af5c6c8e350de0949f45f49038e
function clock() {
    const today = new Date();
    let hour = today.getHours();
    let min = today.getMinutes();
    let sec = today.getSeconds();
    hour = timeFormat(hour);
    min = timeFormat(min);
    sec = timeFormat(sec);
    const clock_fields = document.getElementsByClassName("clock");
    for (let field of clock_fields){
        console.log(field);
        field.textContent = hour + ":" + min + ":" + sec;
    }
    setInterval(clock, 1000);
    
}
function timeFormat(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10    
    return i;
}*/
function clock(){
    setInterval(() => display_clock(new Date().toLocaleTimeString()),1000);
}
function display_clock(string){
    const clock_fields = document.getElementsByClassName("clock");
    for (let field of clock_fields){
        field.textContent = string;
    }
}

var attendance_data = {"records": []};
var confirm_txt = "";
var confirm_btnList = [];
function clockTech(){
    //get time detail
    const hour = (new Date().getHours());
    const min =  (new Date().getMinutes());
    const sec = (new Date().getSeconds());
    //change field_time class
    this.lastElementChild.setAttribute("class", "clocked");
    //disable button
    this.disabled = true;
    confirm_btnList.push(this);

    //log and append time detail
    var record = {
        "email": this.value,        // ** SECURITY EXPOSE
        "clocked": {
            "hour": hour,
            "min": min,
            "sec": sec
        } 
    }
    //prepare info for confirm step
    for (i = 0; i < technicians_data.length; i++){
        var key = "email";
        if (technicians_data[i][key] == this.value){
            key = "name";
            const name_arr = Object.values(technicians_data[i][key])
            const temp_txt = `Technician: ${name_arr[0]} ${name_arr[1]}\n` + 
                            `Clocked time: ${hour}:${min}:${sec}`;
            if (confirm_txt.length == 0 ){
                confirm_txt += temp_txt;
            }else{
                confirm_txt += "\n\n".concat(temp_txt);
            }
        }
    }
    attendance_data['records'].push(record);
    
}

window.onload = checkGrid_enableBtn(0);
// Tech Attendant Checkin | Disable grid if all empty---runtime=0 : window.onload---------------
function checkGrid_enableBtn(runtime){                //runtime=1 : function load
    var checkin_btn = document.getElementsByClassName("checkin_btn");
    //if this function call by window load, just enable buttons
    if (runtime == 0){
        for (var i = 0; i < checkin_btn.length; i++){
            checkin_btn[i].addEventListener("click", clockTech);
        }
    //if function call by other function, then check length of buttons list
    //list == 0, change class name for buttons container div (to hide it)
    //list >= 0, enable div and buttons in the list.
    } else {
        if (checkin_btn.length == 0){
            const div_grid = document.getElementsByClassName("checkin_grid")[0];
            div_grid.setAttribute("class", "checkin_grid_hidden");
            
            const submit_checkin = document.getElementById("submit_checkin");
            submit_checkin.setAttribute("disabled", "true");
        }else{
            const div_grid = document.getElementsByClassName("checkin_grid")[0];
            div_grid.setAttribute("class", "checkin_grid");
            for (var i = 0; i < checkin_btn.length; i++){
                checkin_btn[i].addEventListener("click", clockTech);
                //checkin_btn[i].time_field = checkin_btn[i].firstElementChild;
            }
            
            const submit_checkin = document.getElementById("submit_checkin");
            submit_checkin.removeAttribute("disabled");
        }
    }
}



// Add Tech (new) into attendance list
function addTech(){     
    var selected_tech = document.getElementsByName("technician_id")[0];         // ** SECURITY EXPOSE
    selected_tech = selected_tech.options[selected_tech.selectedIndex].value;   // ** SECURITY EXPOSE
    var count = 0
    var key = "email";

    //check if selected tech already in scheduled list
    for (i = 0; i < scheduled_data.length; i++){
        if (selected_tech == scheduled_data[i][key]){   // ** SECURITY EXPOSE
            count += 1;
            break;
        }
    }
    //NOT in scheduled list
    if (count == 0){
        for (i = 0; i < technicians_data.length; i++){
            if (selected_tech == technicians_data[i][key]){ // ** SECURITY EXPOSE
                key = "name";
                var name_arr = Object.values(technicians_data[i][key]);
                if (confirm(`"Add ${name_arr[0]} ${name_arr[1]} into attendance list?"`)){
                    //create button for new tech
                    const new_elem = document.createElement("button");
                    new_elem.setAttribute("type", "button");
                    new_elem.setAttribute("class", "checkin_btn");
                    new_elem.setAttribute("value", selected_tech);      // ** SECURITY EXPOSE
                    
                    //create time field for button
                    const time_field = document.createElement("span");
                    time_field.setAttribute("class", "clock");
                
                    //include tech name, timefield into button
                    new_elem.appendChild(document.createTextNode(`${name_arr[0]} ${name_arr[1]}`));
                    new_elem.appendChild(document.createElement("br"));
                    new_elem.appendChild(time_field);

                    //include button into div (open div if div empty)
                    var div_grid = document.getElementsByClassName("checkin_grid");
                    if (div_grid.length == 0){
                        div_grid = document.getElementsByClassName("checkin_grid_hidden")[0];
                        div_grid.setAttribute("class", "checkin_grid");
                        div_grid.appendChild(new_elem);
                        const submit_checkin = document.getElementById("submit_checkin");
                        submit_checkin.removeAttribute("disabled");
                    }else{
                        div_grid[0].appendChild(new_elem);
                    }
                    
                    //push new tech data into schedule
                    scheduled_data.push({
                        "email": selected_tech,     // ** SECURITY EXPOSE
                        "name": {
                            "first_name": name_arr[0],
                            "last_name": name_arr[1]
                        }
                    });
                    // add this new button into listener event
                    new_elem.addEventListener("click", clockTech);
                }
            }
        }
    }else{
        window.alert("This technician is already in attendance list!");
    }
}

function resetAttendance(){
    //clear (reset) confirm data
    confirm_txt = "";
    attendance_data = {"records": []};
    
    //unblock buttons, set time_field (by change class)
    //then clear confirm button data
    for (i = 0; i < confirm_btnList.length; i++){
        confirm_btnList[i].disabled = false;
        confirm_btnList[i].lastElementChild.setAttribute("class", "clock");
    }
    confirm_btnList = [];

}

function postAttendance(){
    //alert if nothing to submit
    if (attendance_data['records'].length === 0){
        alert("Nothing to submit!!")
    } else {
        //if user confirm to submit
        if (confirm(confirm_txt)){
            //remove buttons in list from display
            for (i = 0; i < confirm_btnList.length; i++){
                confirm_btnList[i].remove();
            }
            //recheck grid for display(grid and submit btn)
            checkGrid_enableBtn(1);
            //Ajax post after Json the data
            data = JSON.stringify(attendance_data)
            csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            var url = "/manager/"
            $.ajax({
                url: url + "attendance/",
                type: "POST",
                dataType: "json",
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    data
                },
                success: (data) => {
                    console.log(data);

                },
                error: (error) => {
                    console.log(error);
                },
            });
            resetAttendance();
        }
    }
}

