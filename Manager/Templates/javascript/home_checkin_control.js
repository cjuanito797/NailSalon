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


// Tech Attendant Checkin---------------------
var checkin_btn = document.getElementsByClassName("checkin_btn");
for (var i = 0; i < checkin_btn.length; i++){
    checkin_btn[i].addEventListener("click", checkinNewTech);
    checkin_btn[i].time_field = checkin_btn[i].firstElementChild;
}

// Add Tech (new) into attendance list
function addTech(){     
    var selected_tech = document.getElementsByName("technician_id")[0];         // ** SECURITY EXPOSE
    selected_tech = selected_tech.options[selected_tech.selectedIndex].value;   // ** SECURITY EXPOSE
    var count = 0
    var key = "email";
    for (i = 0; i < scheduled_data.length; i++){
        if (selected_tech == scheduled_data[i][key]){   // ** SECURITY EXPOSE
            count += 1;
            break;
        }
    }
    if (count == 0){
        for (i = 0; i < technicians_data.length; i++){
            if (selected_tech == technicians_data[i][key]){ // ** SECURITY EXPOSE
                key = "name";
                var name_arr = Object.values(technicians_data[i][key])
                if (confirm(`"Add ${name_arr[0]} ${name_arr[1]} into attendance list?"`)){
                    
                    const new_elem = document.createElement("button");
                    new_elem.setAttribute("type", "button");
                    new_elem.setAttribute("class", "checkin_btn");
                    new_elem.setAttribute("value", selected_tech);      // ** SECURITY EXPOSE

                    const time_field = document.createElement("span");
                    time_field.setAttribute("class", "clock");
                    //time_field.setAttribute("name", "");
                    //time_field.setAttribute("value", "");
                    //time_field.readOnly = true;
                
                    new_elem.appendChild(document.createTextNode(`${name_arr[0]} ${name_arr[1]}`));
                    new_elem.appendChild(document.createElement("br"));
                    new_elem.appendChild(time_field);

                    const div_grid = document.getElementsByClassName("checkin_grid")[0];
                    div_grid.appendChild(new_elem);

                    scheduled_data.push({
                        "email": selected_tech,     // ** SECURITY EXPOSE
                        "name": {
                            "first_name": name_arr[0],
                            "last_name": name_arr[1]
                        }
                    });
                    new_elem.addEventListener("click", checkinNewTech);
                    console.log(scheduled_data);
                }else{
                    console.log("bad");
                }
            }
        }
    }else{
        window.alert("This technician is already in attendance list!");
    }
}


function checkinNewTech(event){
    const hour = (new Date().getHours());
    const min =  (new Date().getMinutes());
    const sec = (new Date().getSeconds());
    this.lastElementChild.setAttribute("class", "clocked");
    this.disabled = true;

    var record = {
        "email": this.value,        // ** SECURITY EXPOSE
        "clocked": {
            "hour": hour,
            "min": min,
            "sec": sec
        } 
    }
    console.log(record);
}




function postAttendance(){
    /*
    if (document.querySelector('input[name="appointment_id"]')) {
        document.querySelectorAll('input[name="appointment_id"]').forEach((elem) => {
            elem.addEventListener("change", function(event) {
                var item = event.target.value;
                var url = "/manager/"
                $.ajax({
                    url: url,//+item+"/",
                    type: "POST",
                    dataType: "json",
                    data: {
                        csrfmiddlewaretoken: '{{ csrf_token }}',
                        appointment_id: item
                    },
                    success: (data) => {
                        console.log(data);

                    },
                    error: (error) => {
                        console.log(error);
                    },
                });
                window.location.assign(url + item + "/")
            });
        });;
    }
    */
}

