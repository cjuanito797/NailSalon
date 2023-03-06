// Popup Modify Modal -------------------------------------
// Get the modal and element next modal (contain input data to pass)
var modal = document.getElementById("modal");
var input = modal.firstElementChild;
    // Get list of buttons that opens the modal
var a_btn = document.querySelectorAll("[id='a_modify']");
var s_btn = document.querySelectorAll("[id='s_modify']");
    // When the user clicks on the appointment control button, open the modal
for (i = 0; i < a_btn.length; i++){
    a_btn[i].onclick = function() {
        //display modal
        modal.style.display = "block";
        //display timeslot (appointment can has time modifying)
        document.getElementById("div_modal_timeslot").style.display = "block";

        //remove Random Button uses in Sale modify
        var btn = document.querySelectorAll("[id='modal_btn']");
        for (var h = 0; h < btn.length; h++){
            if(btn[h].getAttribute("name") == "technician_id"){
                btn[h].style.display = "none";
            }
        }
        

        //set first cell in timetable hide behind the modal
        document.getElementById("first_cell").style.zIndex = "1";

        //set modal submit button so it can reference appointment
        modal.lastElementChild.lastElementChild.setAttribute("name", "appointment_btn")

        input.setAttribute("name", "appointment_id");
        input.setAttribute("value", this.value);
    }
}


    // When the user clicks on the sale Modify button, open the modal
for (i = 0; i < s_btn.length; i++){
    s_btn[i].onclick = function() {
        //display modal
        modal.style.display = "block";

        //display Randome Button uses in Sale modify
        var btn = document.querySelectorAll("[id='modal_btn']");
        for (var h = 0; h < btn.length; h++){
            if(btn[h].getAttribute("name") == "technician_id"){
                btn[h].style.display = "block";
            }
        }
        //disable timeslot (sales do not need time modify)
        document.getElementById("div_modal_timeslot").style.display = "none";
        //set first cell in timetable hide behind the modal
        first_cell = document.getElementById("first_cell").style.zIndex = "1";

        //set modal submit button so it can reference sale
        modal.lastElementChild.lastElementChild.setAttribute("name", "sale_btn")

        input.setAttribute("name", "sale_id");
        var sale_id_elem = document.querySelectorAll("[name='sale_id']");
        for (var z = 0; z < sale_id_elem.length; z++){
            if (sale_id_elem[z].checked){
                input.setAttribute("value", sale_id_elem[z].value);
            }
        }
    }
}

var btn = document.querySelectorAll("[id='modal_btn']");
for (var i = 0; i < btn.length; i++){
    if(btn[i].getAttribute("name") == "technician_id"){
        btn[i].style.display = "block";
        btn[i].onclick = function(){
            this.previousElementSibling.add((new Option("-- Random --", "random")), 0);
            this.previousElementSibling.selectedIndex = "0";
            
            
            if (confirm("Replace next random technician into this sale?") == true){
                
                for (var j = 0; j < btn.length; j++){
                    if(btn[j].getAttribute("name") == "sale_btn"){
                        btn[j].click()
                    }
                }
            }else{
                this.previousElementSibling.options[0].remove();
            }

            
        };
    }
}










// Popup Add-Tech(Attendant) Modal -------------------------
var add_checkinModal = document.getElementById("model_addCheckin");
var add_checkin = document.getElementById("add_checkin");
add_checkin.onclick = function(){
    add_checkinModal.style.display = "block";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        document.getElementById("first_cell").style.zIndex = "2";
    }
    else if (event.target == add_checkinModal) {
        add_checkinModal.style.display = "none";
        document.getElementById("first_cell").style.zIndex = "2";
    }
}


// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close");
// When the user clicks on <span> (x) (**on all model), close the modal
for (i = 0; i < span.length; i++){
    span[i].onclick = function() {
        modal.style.display = "none";
        add_checkinModal.style.display = "none";
        document.getElementById("first_cell").style.zIndex = "2";
    }
}


