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
        //enable timeslot (appointment can has time modifying)
        var timefield = document.querySelectorAll("[name='timeslot']")
        for (var j = 0; j < timefield.length; j++){
            timefield[j].disabled = false;
        }
        //set modal submit button so it can reference appointment
        modal.lastElementChild.lastElementChild.setAttribute("name", "appointment_btn")

        input.setAttribute("name", "appointment_id");
        input.setAttribute("value", this.value);
    }
}
    // When the user clicks on the sale control button, open the modal
for (i = 0; i < s_btn.length; i++){
    s_btn[i].onclick = function() {
        //display modal
        modal.style.display = "block";
        //disable timeslot (sales do not need time modify)
        var timefield = document.querySelectorAll("[name='timeslot']")
        for (var j = 0; j < timefield.length; j++){
            timefield[j].disabled = true;
        }

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
    // When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


// Popup New Technician Modal -------------------------
var modal_newtech = document.getElementById("modal_newtech");
function newtech(){
    modal_newtech.style.display = "block";
    const state_dropdown = document.getElementById("state");
        let states = Object.keys(location_data);

        for (i = 0; i < states.length; i++){
            //create option for states dropdown
            const new_elem = document.createElement("option");
            new_elem.setAttribute("value", states[i]);
            new_elem.appendChild(document.createTextNode(`${location_data[states[i]]['name']}`));
            state_dropdown.appendChild(new_elem);
        }
}
function state_onchange(value){
    const city_dropdown = document.getElementById("city");
    let state_info = location_data[value]["cities"];
    let city_name = (Object.keys(state_info));
    for (i = 0; i < city_name.length; i++){
        //create option for cities dropdown
        const new_elem = document.createElement("option");

        new_elem.setAttribute("value", city_name[i]);
        new_elem.appendChild(document.createTextNode(city_name[i]));
        city_dropdown.appendChild(new_elem);
    }
}
function city_onchange(value){
    console.log(value)
    const zipcode_dropdown = document.getElementById("zipcode");

    
    let zipcode= location_data[value]["cities"];
    let city_name = (Object.keys(state_info));
    for (i = 0; i < city_name.length; i++){
        //create option for cities dropdown
        const new_elem = document.createElement("option");

        new_elem.setAttribute("value", city_name[i]);
        new_elem.appendChild(document.createTextNode(city_name[i]));
        city_dropdown.appendChild(new_elem);
    }
}



// Popup Add-Tech(Attendant) Modal -------------------------
var add_checkinModal = document.getElementById("model_addCheckin");
var add_checkin = document.getElementById("add_checkin");
add_checkin.onclick = function(){
    add_checkinModal.style.display = "block";
}



// close when user click outside of the modal
window.onclick = function(event) {
    if (event.target == add_checkinModal) {
        add_checkinModal.style.display = "none";
    }
}
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close");
// When the user clicks on <span> (x) (**on all model), close the modal
for (i = 0; i < span.length; i++){
    span[i].onclick = function() {
        modal.style.display = "none";
        add_checkinModal.style.display = "none";
        modal_newtech.style.display = "none";
    }
}


