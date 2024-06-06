function formValidation(key, value, id) {
    var errorMessage = $("#" + id).next(".error-message");
    isValid = true

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
        // Add more cases for other fields as required
        default:
            break;
    }
    console.log(isValid, "invalidation")
    return isValid
}