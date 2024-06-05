var formData = {
    "office-name": "",
    "office-purpose":""
}
var invite_employees = []
var employee = {}
var accounts = []

function stateChange(key, value, id) {
    formValidation(key, value, id)
    formData[key] = value
    console.log(formData, "formData")
}

function addAccounts(){
    account = {}
    // Append the account object to the accounts list
    accounts.push(account)
   return account
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
    console.log(accounts, "getAfterHyphen")
    console.log(accounts, "account accunts")
}
 
function StateinviteEmployee(index, key, value){
    isValid = formValidation(key, value, "chip-input")
    console.log(index, key, value, ":PPPPPPPPPPPPPPPPPPP")
    if(isValid){
        invite_employees[index][key]=value

    }
    console.log(invite_employees,"invite_employees")
    return isValid
}

function getEmployeeRole(){
    var index = invite_employees.length - 1
    var value = activeRoleName = $('.profile-role.active-role').attr('name');
    invite_employees[index]['role']=value
    employee = {}
}


function cancelInviteEmployee(id){
    console.log(id, "idididididdidid")
    index = getAfterHyphen(id)
    console.log(index, "indexindexindexindex")
    invite_employees.splice(index, 1);
    console.log(invite_employees, "invite_employeesinvite_employeesinvite_employees")
}

function removeBankAccount(id){
    index = getAfterHyphen(id)
    accounts.splice(index, 1);
    console.log(accounts, "removeBankAccount removeBankAccount")
}


function PostOfficeForm(){
    data = {
        "office": formData,
        "bank_accounts": accounts,
        "invite_employee": invite_employees
    }
    console.log(data, "datdatatada")
}