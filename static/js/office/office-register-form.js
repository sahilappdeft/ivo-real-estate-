var formData = {
    "name": "",
    "purpose":""
}
var invite_employees = {}
var employee = {}
var accounts = {}

function stateChange(key, value, id) {
    formValidation(key, value, id)
    formData[key] = value
}

function addAccounts(counter){
    account = {}
    // Append the account object to the accounts list
    accounts[counter.toString()]=account
}

function getAfterHyphen(str) {
    // Split the string at the hyphen (-)
    var parts = str.split("-");
  
    // If there's no hyphen, return the original string
    if (parts.length === 1) {
      return str;
    }
  
    // Return the part after the hyphen (index 1)
    return parts[1];
  }

function stateAccount(id, value, key){
    index = getAfterHyphen(id)
    accounts[index][key] = value
}
 
function StateinviteEmployee(index, key, value){
    isValid = formValidation("email", value, "chip-input")
    if(isValid){
        invite_employees[index.toString()][key]=value

    }
    return isValid
}

function getEmployeeRole(){
    // Get an array of object keys
    var keysArray = Object.keys(invite_employees);
    // Access the last key of the array
    var lastKey = keysArray[keysArray.length - 1];
    var value = activeRoleName = $('.profile-role.active-role').attr('name');
    invite_employees[lastKey]['role']=value
    employee = {}
}


function cancelInviteEmployee(id){
    index = getAfterHyphen(id)
    delete invite_employees[index]
}

function removeBankAccount(id){
    index = getAfterHyphen(id)
    delete accounts[index]
}


function PostOfficeForm(){
    var accounts_data = Object.values(accounts);
    var invite_employees_data =  Object.values(invite_employees);
    var data = {
        "office": formData,
        "bank_accounts": accounts_data,
        "invite_employee": invite_employees_data
    };
    console.log(data, "datdatatada");

    // Retrieve token from local storage
    var accessToken = localStorage.getItem('access_token');
    console.log(accessToken, "accessToken")
    $.ajax({
        type: 'POST',
        url: BASE_URL + 'api/office/offices/',
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        beforeSend: function(xhr) {
            // Include token in the request header
            xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken);
        },
        success: function(response) {
            console.log('POST request successful:', response);
            // Handle success response
        },
        error: function(xhr, status, error) {
            console.error('Error sending POST request:', error);
            // Handle error response
        }
    });
}


function companyRole(){

    // Retrieve token from local storage
    var accessToken = localStorage.getItem('access_token');
    console.log(accessToken, "accessToken accessTokenaccessToken")
    $.ajax({
        type: 'GET',
        url: BASE_URL + 'api/office/roles/',
        beforeSend: function(xhr) {
            // Include token in the request header
            xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken);
        },
        success: function(response) {
            console.log('GET request successful:', response);
            // Handle success response
            updateProfileRoles(response);
        },
        error: function(xhr, status, error) {
            console.error('Error sending GET request:', error);
            // Handle error response
        }
    });
}

function updateProfileRoles(roles) {
    // Get all div elements with the class 'profile-role'
    var profileRoles = document.querySelectorAll('.profile-role');

    // Ensure the number of roles matches the number of profile-role elements
    if (roles.length !== profileRoles.length) {
        console.error('Mismatch between roles and profile-role elements');
        return;
    }

    // Loop through each profile-role element and update the name attribute
    roles.forEach((role, index) => {
        profileRoles[index].setAttribute('name', role.id);
    });
}


// Function to update preview modal content
function updateModalContent(data) {
    document.querySelector('.preview-data.office-name').textContent = data.name || '';
    document.querySelector('.preview-data.office-nickname').textContent = data.office_nickname || '';
    document.querySelector('.preview-data.office-purpose').textContent = data.purpose || '';
    document.querySelector('.preview-data.street').textContent = data.street || '';
    document.querySelector('.preview-data.street-no').textContent = data.address || '';
    document.querySelector('.preview-data.zipcode').textContent = data.zipcode || '';
}

// Example function to open the modal and update content
function openPreviewModal() {
    updateModalContent(formData);
    $('#previewmodal').modal('show');
}