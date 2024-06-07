$(document).ready(function () {
    // Function to gather OTP input values
    function getOtp() {
        var otp = "";
        $(".otp").each(function () {
            otp += $(this).val();
        });
        return otp;
    }

    // Function to extract email from URL parameter
    function getEmailFromUrl() {
        var urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('email');
    }

    function decodeEmail(encodedEmail) {
        let decodedEmail = '';
        for (let i = 0; i < encodedEmail.length; i++) {
          decodedEmail += String.fromCharCode(encodedEmail.charCodeAt(i) - 1);
        }
        return decodedEmail;
    }

    // Event listener for form submission
    $('#submitbtn').click(function () {
        event.preventDefault(); // Prevent the default form submission

        // Get email and OTP
        var email = getEmailFromUrl();
        var decodeMail = decodeEmail(email);
        console.log(decodeMail, ":::POO")

        var otp = getOtp();
        // AJAX request
        $.ajax({
            url: BASE_URL + 'api/auth/verify-email/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                email: decodeMail,
                otp: otp
            }),
            success: function(response) {
                console.log('Verification successful');
                $("#successMessage").text(response.message).fadeIn().delay(3000).fadeOut(); // Display success message and fade out after 3 seconds
                $("#errorMessage").hide(); // Hide error message if it's currently displayed
                $("#successMessage").show(); // Show success message
                window.location.href = BASE_URL;

            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText); // Log the error response to the console
                $("#errorMessage").text('OTP Invalid. Please try again.').fadeIn(); // Show error message
                $("#successMessage").hide(); // Hide success message if it's currently displayed
                $("#errorMessage").show(); // Show error message
            }
        });
    });

    // Function to handle resend link click
    $("#resendLink").on("click", function(event) {
        event.preventDefault(); // Prevent the default behavior of the link
        
        // Get the email address from the user 
        var email = getEmailFromUrl();
        var decodeMail = decodeEmail(email);
  
        // Prepare the data to be sent in the POST request
        var postData = {
          'email': decodeMail
        };
  
        // Send AJAX request to the API endpoint
        $.ajax({
          type: 'POST',
          url: BASE_URL + 'api/auth/send-otp/verify/',
          data: postData, // Send email data as JSON
          dataType: 'json', // Specify JSON as the expected response type
          success: function(response) {
            console.log('resend otp');
          },
          error: function(xhr, status, error) {
            console.log('failed');

          }
        });
      });

});