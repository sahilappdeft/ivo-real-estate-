import { encodeEmail } from './common.js';


$(document).ready(function() {
    $('#forgotPasswordForm').on('submit', function(event) {
      event.preventDefault(); // Prevent the default form submission

      var email = $('#inputEmail').val();
      var encdEmail = encodeEmail(email);
        
      console.log(encdEmail, "encodeEmail")
      // Redirect to the OTP verification page with the encoded email as a URL parameter
      console.log(window.location.href, "window.location.href")
      window.location.href = '/?email=' + encdEmail;
    });
  });