$(document).ready(function() {
    // Regular expressions for email and password validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*[0-9]).{8,}$/;
  
    // Function to validate email
    function validateEmail(email) {
      return emailRegex.test(email);
    }
  
    // Function to validate password
    function validatePassword(password) {
      return passwordRegex.test(password);
    }
  
    function encodeEmail(email) {
      let encodedEmail = '';
      for (let i = 0; i < email.length; i++) {
        encodedEmail += String.fromCharCode(email.charCodeAt(i) + 1);
      }
      return encodedEmail;
    }
  
    // Email input event listener
    $("#inputEmail").on("input", function() {
      const email = $(this).val();
      console.log(email)
      if (!validateEmail(email)) {
          $("#emailError").text("Please enter a valid email address.").css("visibility", "visible");
      } else {
          $("#emailError").text("");
      }
    });
  
    // Clear error message when user starts typing in first name field
    $("#inputFirstName").on("input", function() {
        $("#firstNameError").text("");
    });
  
    // Clear error message when user starts typing in last name field
    $("#inputLastName").on("input", function() {
        $("#lastNameError").text("");
    });
  
    // Password input event listener
    $("#inputPassword").on("input", function() {
      const password = $(this).val();
      if (!validatePassword(password)) {
          $("#passwordError").text("Password must be at least 8 characters long and contain at least one uppercase letter, one special character, and one digit.").css("visibility", "visible");
      } else {
          $("#passwordError").text("");
      }
    });
  
    // Confirm password input event listener
    $("#inputConfirmPassword").on("input", function() {
      const confirmPassword = $(this).val();
      const password = $("#inputPassword").val();
      if (password !== confirmPassword) {
          $("#confirmPasswordError").text("Passwords do not match.").css("visibility", "visible");
      } else {
          $("#confirmPasswordError").text("");
      }
    });
  
    // Clear error message when user clicks on terms checkbox
    $("#flexCheckDefault").on("click", function() {
        $("#termsError").text("");
    });
  
    // Function to check if all fields are valid
    function validateForm() {
        const email = $("#inputEmail").val();
        const firstName = $("#inputFirstName").val();
        const lastName = $("#inputLastName").val();
        const password = $("#inputPassword").val();
        const confirmPassword = $("#inputConfirmPassword").val();
        const termsCheck = $("#flexCheckDefault").is(":checked");
  
        let isValid = true;
  
        // Check email
        if (!email || !validateEmail(email)) {
            $("#emailError").text("Please enter a valid email address.").css("visibility", "visible");
            isValid = false;
        } else {
            $("#emailError").text("");
        }
  
        // Check first name
        if (!firstName) {
            $("#firstNameError").text("First name is required.").css("visibility", "visible");
            isValid = false;
        } else {
            $("#firstNameError").text("");
        }
  
        // Check last name
        if (!lastName) {
            $("#lastNameError").text("Last name is required.").css("visibility", "visible");
            isValid = false;
        } else {
            $("#lastNameError").text("");
        }
  
        // Check password
        if (!password) {
            $("#passwordError").text("Password is required.").css("visibility", "visible");
            isValid = false;
        } else if (!passwordRegex.test(password)) {
            $("#passwordError").text("Password must be at least 8 characters long and contain at least one uppercase letter, one special character, and one digit.").css("visibility", "visible");
            isValid = false;
        } else {
            $("#passwordError").text("");
        }
  
        // Check confirm password
        if (!confirmPassword) {
            $("#confirmPasswordError").text("Please confirm your password.").css("visibility", "visible");
            isValid = false;
        } else if (password !== confirmPassword) {
            $("#confirmPasswordError").text("Passwords do not match.").css("visibility", "visible");
            isValid = false;
        } else {
            $("#confirmPasswordError").text("");
        }
  
        // Check terms and conditions
        if (!termsCheck) {
            $("#termsError").text("Please accept the terms and conditions.").css("visibility", "visible");
            isValid = false;
        } else {
            $("#termsError").text("");
        }
  
        return isValid;
    }
  
    // Submit form and validate
    $("#submitBtn").click(function(event) {
        // Clear previous error messages
        $(".error-message").text("");
  
        // Validate form
        if (!validateForm()) {
            // If form is not valid, prevent submission
            event.preventDefault();
            return;
        }
  
        // If form is valid, send AJAX request
        var formData = {
            'email': $("#inputEmail").val(),
            'first_name': $("#inputFirstName").val(),
            'last_name': $("#inputLastName").val(),
            'password': $("#inputPassword").val(),
            'confirmPassword': $("#inputConfirmPassword").val()
        };
  
        $.ajax({
            type: 'POST',
            url: BASE_URL + 'api/auth/signup/',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                // Handle success response
                console.log(response);
  
                // Assuming response contains user email
                var userEmail = formData.email;
  
                // Redirect to verification page with user email as query parameter
                window.location.href = BASE_URL + 'api/auth/verify-email/?email=' + encodeEmail(userEmail);
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error(xhr.responseText);
            }
        });
    });
  });