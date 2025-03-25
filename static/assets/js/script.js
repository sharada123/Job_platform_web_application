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

    function total_applications(jobId) {
        console.log("Fetching total applications for job:", jobId);

        fetch(`/total_applications/${jobId}/`, { 
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' } 
        })
        .then(response => response.json())
        .then(data => {
            Swal.fire({
                title: "Application Count",  // 📝 Custom Title
                text: "Total Applications: " + data.total_applications,
                icon: "info",  // 🔔 You can change this to success, warning, error
                confirmButtonText: "OK",
            });
        })
        .catch(error => {
            console.error("Error fetching total applications:", error);
            Swal.fire({
                title: "Error!",
                text: "Could not fetch application count.",
                icon: "error",
                confirmButtonText: "OK",
            });
        });
    }

