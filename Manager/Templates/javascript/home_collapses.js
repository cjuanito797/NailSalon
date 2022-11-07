// Display Appointment Collapsible Button--------------------
var coll = document.getElementsByClassName("collapsible");
var i;
for (i = 0; i < coll.length; i++){
    coll[i].addEventListener("click", function(){
        this.classList.toggle("active");
        var content = (this.parentElement).nextElementSibling;
        var a_control = this.nextElementSibling;
        if (content.style.display === "block"){
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
        this.scrollIntoView()
    });
}
var ap = document.getElementsByClassName("appointment");
for (i = 0; i < ap.length; i++){
    ap[i].addEventListener("mouseover", function(){
        var appointments = this.firstElementChild;
        var a_control = this.lastElementChild;
            a_control.style.display = "block";
    });
    ap[i].addEventListener("mouseout", function(){
        var a_control = this.lastElementChild;
            a_control.style.display = "none";
    });
}
// Display Appointment Collapsible Button-----------------END