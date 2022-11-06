// Tech Attendant Checkin---------------------
var checkin_btn = document.getElementsByClassName("checkin_btn")
for (i = 0; i < checkin_btn.length; i++){
    checkin_btn[i].onclick = function() {
        console.log(this.value)
        console.log(new Date().getHours())
        console.log(new Date().getMinutes())
        console.log(new Date().getSeconds())
        this.disabled = true;
    }
}