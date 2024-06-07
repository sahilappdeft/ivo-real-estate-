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

    // Event listener for form submission
    $('#submitbtn').click(function () {
        event.preventDefault(); // Prevent the default form submission

        // Get email and OTP
        var email = getEmailFromUrl();
        var otp = getOtp();

        // Check for empty input fields
        var emptyFields = $('.otp').filter(function() {
            return $(this).val() === '' 
        });

        if (emptyFields.length > 0) {
            $('#emailError').text('Please fill in all OTP fields.');
            return; // Stop further execution
        }

        // Redirect to verification page with user email as query parameter
        window.location.href = BASE_URL + 'api/auth/forgot-password/?email=' + email+'&otp='+otp;

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
          url: BASE_URL + 'api/auth/send-otp/forgot/',
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