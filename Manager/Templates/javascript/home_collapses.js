// Display Appointment Collapsible Button--------------------
var coll = document.getElementsByClassName("collapsible");
var i;
for (i = 0; i < coll.length; i++){
    coll[i].addEventListener("click", function(){
        this.classList.toggle("active");
        var content = (this.parentElement).nextElementSibling;
        var a_control = this.nextElementSibling;
        if (content.style.display !== "block" && this.classList.contains("active")){
            content.style.display = "block";
        } else {
            content.style.display = "none";
        }
    });
}
var ap = document.getElementsByClassName("appointment");
for (i = 0; i < ap.length; i++){
    ap[i].addEventListener("mouseover", function(){
        var a_control = this.lastElementChild;
            a_control.style.display = "block";
    });
    ap[i].addEventListener("mouseout", function(){
        var a_control = this.lastElementChild;
            a_control.style.display = "none";
    });
}
// Display Appointment Collapsible Button-----------------END

// Display/Hide Appointment on dates
function sort_appointment(){
    //get selected value
    const dropdown = document.getElementById("apt_date");
    const selectedValue = dropdown.options[dropdown.selectedIndex].value;
    //get all elements
    const all_appointments = document.getElementsByClassName("appointment")
    const all_contents = document.getElementsByClassName("content")
    //if selected value = "all", then display all appointment and hide their content
    if (selectedValue == "all"){
        for (i = 0; i < all_appointments.length; i++){
            all_appointments[i].style.display = "block";
            all_contents[i].style.display = "none";
            
        }
    //if not 'all', then loop through appointment
    }else{
        for (i = 0; i < all_appointments.length; i++){
            //if this appointment id = selected value, then display the appointment
            if (all_appointments[i].id == selectedValue){
                all_appointments[i].style.display = "block";
                all_contents[i].style.display = "none";
            //else, hide the appointment, and remove "active class" (remove click color)
            }else{
                all_appointments[i].classList.remove("active");
                all_appointments[i].style.display = "none";
                all_contents[i].style.display = "none";
            }
        }
    }
    //remove all "active class" (remove click color)
    for (i = 0; i < coll.length; i++){
        coll[i].classList.remove("active");
    }
    
}

window.onload = sort_timetable()
// Display/Hide Timetable on dates
function sort_timetable(){
    //get selected value
    const dropdown = document.getElementById("timetable_date");
    const selectedValue = dropdown.options[dropdown.selectedIndex].value;
    //get all elements
    const all_timetable = document.getElementsByClassName("timetable")

    for (i = 0; i < all_timetable.length; i++){
        //if this appointment id = selected value, then display the appointment
        if (all_timetable[i].id == selectedValue){
            all_timetable[i].style.display = "block";
        //else, hide the appointment, and remove "active class" (remove click color)
        }else{
            all_timetable[i].style.display = "none";
        }
    }
    
}