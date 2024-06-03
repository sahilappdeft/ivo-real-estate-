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

 // Function to extract email from URL parameter
 function getEmailFromUrl() {
    var urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('email');
}

 // Function to extract otp from URL parameter
 function getOtpFromUrl() {
  var urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('otp');
}

function decodeEmail(encodedEmail) {
  let decodedEmail = '';
  for (let i = 0; i < encodedEmail.length; i++) {
      decodedEmail += String.fromCharCode(encodedEmail.charCodeAt(i) - 1);
  }
  return decodedEmail;
}