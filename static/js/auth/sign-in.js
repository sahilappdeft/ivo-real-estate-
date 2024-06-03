$(document).ready(function() {
    // Clear error message when user starts typing in email field
    $("#inputEmail").on("input", function() {
        $("#emailError").text("");
    });

    // Clear error message when user starts typing in password field
    $("#inputPassword").on("input", function() {
        $("#passwordError").text("");
    });


    // Submit form and validate
    $("#submitBtn").click(function(event) {
        console.log()
        // Clear previous error messages
        $(".error-message").text("");

        const email = $("#inputEmail").val();
        const password = $("#inputPassword").val();
        // Regular expression for email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Check if email is empty
        if (!email) {
            $("#emailError").text("Email is required.");
            event.preventDefault();
        } else if (!emailRegex.test(email)) { // Check if email is valid
            $("#emailError").text("Please enter a valid email address.");
            event.preventDefault();
        }

        // Check if password is empty
        if (!password) {
            $("#passwordError").text("Password is required.");
            event.preventDefault();
        }

        // Send AJAX request
        var formData = {
            'email': email,
            'password': password,
        };
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/api/auth/login/',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
            // Check if the response contains an access token
            if (response && response.data && response.data.access_token) {
                // Store the access token in the local storage
                localStorage.setItem('access_token', response.data.access_token);
                // Optionally, you can also store the refresh token and token type if needed
                localStorage.setItem('refresh_token', response.data.refresh_token);
                localStorage.setItem('token_type', response.data.token_type);
                //redirecting to a dashboard page
                window.location.href = 'http://127.0.0.1:8000/api/auth/dashboard/';
            } else {
                // Handle the case where the access token is missing in the response
                console.error('Access token not found in the response');
            }
            },
            error: function(response) {
            var error = JSON.parse(response.responseText); // Parse the JSON error response
            $("#errorMessage").text(error.error).fadeIn().delay(3000).fadeOut(); // Show error message
            $("#successMessage").hide(); // Hide success message if it's currently displayed
            $("#errorMessage").show(); 
            }
        });
        
    });

});