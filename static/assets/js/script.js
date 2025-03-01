function send_to_verify() {
    // Hide email section
    document.getElementById('email-section').classList.add('hidden');

    // Show OTP section
    document.getElementById('otp-section').classList.add('show');
}
function show_login(){
   // hide OTP section
    document.getElementById('otp-section').classList.add('hidden'); 

     // Show Login button  section
     document.getElementById('btn-section').classList.add('show');  
}