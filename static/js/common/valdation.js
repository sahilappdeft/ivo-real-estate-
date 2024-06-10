function formValidation(key, value, id) {
    var errorMessage = $("#" + id).next(".error-message");
    let isValid = true
    switch (key) {
        case "name":
        case "address":
        case "street":
        case "city":
        case "zipcode":
        case "country":
        case "city":
        case "city_division":
        case "phone_number":
        case "cost-center":
        case "owner_name":
        case "iban":
        case "bic":
        case "first_name":
        case "last_name":
            // console.log(typeof value, ":::::::::::andr")
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
                errorMessage.text("Field is required").css("display", "block"); 
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
            }
            else{
                errorMessage.text("")
            }
        default:
            break;
    }
    console.log(isValid, "invalidation")
    return isValid
}