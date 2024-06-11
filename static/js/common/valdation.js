function formValidation(key, value, id) {
    inputValue = $("#" + id)
    var errorMessage = $("#" + id).next(".error-message");
    console.log(key, value, id)
    let isValid = true
    switch (key) {
        case "name":
        case "address":
        case "street":
        case "city":
        case "country":
        case "city":
        case "city_division":
        case "cost-center":
        case "owner_name":
        case "iban":
        case "bic":
        case "first_name":
        case "last_name":
            if (value === "") {
                errorMessage.text("Field is required").css("visibility", "visible");
                isValid = false
            } else {
                errorMessage.text("");
            }
            break;
        case "office-purpose":
        case "purpose":
            if (value === "") {
                console.log("DADASDAASDS")
                errorMessage.text("Please select appropriate purpose").css("visibility", "visible");
                isValid = false
            } else {
                errorMessage.text("");
            }
            break;
        case "email":
        case "office_email":
            console.log("email", value)
            if (value === "") {
                errorMessage.text("Field is required").css("visibility", "visible");
                isValid = false
            } else if(!validateEmail(value)){
                errorMessage.text("Please enter a valid email address.").css("visibility", "visible");
                isValid = false
            }else {
                errorMessage.text("");
            }
            break;
        case "password":
            if(!validatePassword(value)){
                 errorMessage.text("Password must be at least 8 characters long and contain at least one uppercase letter, one special character, and one digit.").css("visibility", "visible");
                 isValid = false
            }else if(value === ""){
            errorMessage.text("Field is required").css("visibility", "visible");
            isValid = false 
            }else{
                errorMessage.text("");
            }
           break;
        case "confirm_password":
            var password = $("#password").val();
            console.log(password, value, ":::::::;")
            if(value != password){
                errorMessage.text("Passwords do not match.").css("visibility", "visible");;
                isValid = false
            }else if(value === ""){
                errorMessage.text("Field is required").css("visibility", "visible");
                isValid = false 
            }else{
                errorMessage.text("");
            }
            break;
        case "zipcode":
            const germanZipCodeRegex = /^\d{5}$/;
            if (value === "") {
                errorMessage.text("Field is required").css("visibility", "visible");
                isValid = false
            }else if (value.length > 5) {
                inputValue.val(value.slice(0, 5)); // Slice input to 10 characters
                errorMessage.text("zipcode cannot exceed 5 digits").css("visibility", "visible");
            }else{
                errorMessage.text("")
            }
            break;
        case "phone_number":
            if (value === "") {
                errorMessage.text("Field is required").css("visibility", "visible");
                isValid = false
            }else if (value.length > 10) {
                inputValue.val(value.slice(0, 10)); // Slice input to 10 characters
                errorMessage.text("Phone number cannot exceed 10 digits").css("visibility", "visible");
            } else if (value.length < 8 || (value.length > 8 && value.length < 10)) {
                errorMessage.text("Phone number must be exactly 8 or 10 digits").css("visibility", "visible");
                isValid = false
            } else if (!validatePhoneNumber(value)) {
                errorMessage.text("Please enter a valid phone number").css("visibility", "visible");
                isValid = false
            } else {
                errorMessage.text("").css("visibility", "hidden");
            }
            
            break;
        default:
            break;
    }
    console.log(isValid, "invalidation")
    return isValid
}