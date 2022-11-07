window.csrftoken="{{csrftoken}}";
window.onload = clock();
function clock() {
    const today = new Date();
    let hour = today.getHours();
    let min = today.getMinutes();
    let sec = today.getSeconds();
    hour = timeFormat(hour);
    min = timeFormat(min);
    sec = timeFormat(sec);
    
    var clocks = document.getElementsByClassName("clock");
    
    for (let clock of clocks){
        clock.textContent = hour + ":" + min + ":" + sec;
    }
    setInterval(clock, 1000);
    
  }
function timeFormat(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10    
    return i;
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
        var key = "email"
        if (technicians_data[i][key] == this.value){
            key = "name";
            const name_arr = Object.values(technicians_data[i][key])
            const temp_txt = `Technician: ${name_arr[0]} ${name_arr[1]}\n` + 
                            `Clocked time: ${timeFormat(hour)}:${timeFormat(min)}:${timeFormat(sec)}`;
            if (confirm_txt.length == 0 ){
                confirm_txt += temp_txt;
            }else{
                confirm_txt += "\n\n".concat(temp_txt);
            }

        }
    }
    

    attendance_data['records'].push(record)
}

// Tech Attendant Checkin---------------------
var checkin_btn = document.getElementsByClassName("checkin_btn");
for (var i = 0; i < checkin_btn.length; i++){
    checkin_btn[i].addEventListener("click", clockTech);
    //checkin_btn[i].time_field = checkin_btn[i].firstElementChild;
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
                var name_arr = Object.values(technicians_data[i][key])
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

                    //include button into div
                    const div_grid = document.getElementsByClassName("checkin_grid")[0];
                    div_grid.appendChild(new_elem);

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
    alert("hi")
}

function postAttendance(){
    if (attendance_data['records'].length === 0){
        alert("Nothing to submit!!")
    } else {
        if (confirm(confirm_txt)){
            for (i = 0; i < confirm_btnList.length; i++){
                confirm_btnList[i].remove();
            }
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
        }else{
            console.log("no")
        }
    }
}

