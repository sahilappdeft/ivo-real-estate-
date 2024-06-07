$(document).ready(function () {
    // Real-time password validation
    $('#inputPassword').on('input', function () {
        var password = $(this).val();
        var passwordError = $('#passwordError');

        if (!validatePassword(password)) {
            passwordError.text("Password must be at least 8 characters long and contain at least one uppercase letter, one special character, and one digit.").css("visibility", "visible");
        } else {
            passwordError.text(""); // Clear error message
        }
    });

    // Real-time password confirmation matching
    $('#confirmPassword').on('input', function () {
        var confirmPassword = $(this).val();
        var password = $('#inputPassword').val();
        var confirmPasswordError = $('#confirmPasswordError');

        if (confirmPassword !== password) {
            confirmPasswordError.text("Passwords do not match.").css("visibility", "visible");
        } else {
            confirmPasswordError.text(""); // Clear error message
        }
    });

    // Form submission
    $("#submitBtn").click(function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Perform additional validation
        var password = $('#inputPassword').val();
        var confirmPassword = $('#confirmPassword').val();

        // Check password length and validity
        if (!validatePassword(password)) {
            $('#passwordError').text("Password must be at least 8 characters long and contain at least one uppercase letter, one special character, and one digit.");
            return; // Stop form submission
        }

        // Check password confirmation
        if (confirmPassword !== password) {
            $('#confirmPasswordError').text("Passwords do not match.");
            return; // Stop form submission
        }

        // If form is valid, send AJAX request
        var email = getEmailFromUrl();
        console.log(email, "email")
        var decodedEmail = decodeEmail(email);
        var formData = {
            'otp': getOtpFromUrl(),
            'email': decodedEmail,
            'password': password,
            'confirmPassword': confirmPassword
        };

        $.ajax({
            type: 'POST',
            url: BASE_URL + 'api/auth/forgot-password/',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                // Handle success response
                console.log(response);

                // Redirect to success page
                window.location.href = BASE_URL + 'api/auth/forgot-password-sucess/';
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