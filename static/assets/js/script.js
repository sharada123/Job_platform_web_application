// Remove alert after 1 second
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
      let alertBox = document.getElementById("message-alert");
      if (alertBox) {
        alertBox.style.opacity = "0";
       
      }
    }, 1000); 
  });