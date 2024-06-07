$(document).ready(function() {

    // Regular expression for email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Clear error message when user starts typing in email field
    $("#inputEmail").on("input", function() {
        $("#emailError").text("");
    });

    // Function to check if all fields are valid
    function validateForm(email) {
        let isValid = true;
        // Check if email is empty
        if (!email) {
            $("#emailError").text("Email is required.").css("visibility", "visible");
            event.preventDefault();
            isValid = false
            }
        else if (!emailRegex.test(email)) { // Check if email is valid
            $("#emailError").text("Please enter a valid email address.").css("visibility", "visible");
            event.preventDefault();
            isValid = false
            }
        return isValid
        
    }    

    $("#submitBtn").click(function(event) {
        console.log("PPPPPPPPPPPPPPPPPPPPPPP")
        // Clear previous error messages
        $(".error-message").text("");
        const email = $("#inputEmail").val();

        console.log(email, ":::::::::::::::::::::::::::::::::::::::::::")

        // Validate form
        if (!validateForm(email)) {
            // If form is not valid, prevent submission
            event.preventDefault();
            return;
        }
        // Prepare the data to be sent in the POST request
        var postData = {
            'email': email
        };

        // Send AJAX request to the API endpoint
        $.ajax({
            type: 'POST',
            url: BASE_URL + 'api/auth/send-otp/forgot/',
            data: postData, // Send email data as JSON
            dataType: 'json', // Specify JSON as the expected response type
            success: function(response) {
                window.location.href = BASE_URL + 'api/auth/forgot-otp/?email=' + encodeEmail(email);
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