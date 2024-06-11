function SetupAccount(){
    // Perform form validation
    var isValid = true;
    $(".form-control").each(function() {
        var id = $(this).attr('id'); 
        var name =  $(this).attr('name'); 
        var value = $(this).val().trim(); 
        // Check validation
        if (!formValidation(name, value, id)) {
            isValid = false;
        }
    });

    // If form is valid, submit via AJAX
    if (isValid) {
        var urlParams = new URLSearchParams(window.location.search);
        var token = urlParams.get('token');
        $.ajax({
            url: BASE_URL + 'api/auth/setup-account/?token='+ token,
            method: 'POST',
            data: $('#multi-step-form').serialize(), // Serialize form data
            success: function(response) {
                // Handle success
                toastr.success(response.message); // Display success toaster

            },
            error: function(xhr, status, error) {
                // Handle error
                var errorMessage = "An error occurred"; // Default error message
                if (xhr.responseText) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        console.log(response.error, "response")
                        errorMessage = response.error || errorMessage;
                    } catch (e) {
                        console.error("Error parsing JSON response:", e);
                    }
                }
                toastr.error(errorMessage); // Display error toaster
            
            }
        });
    }
  
}