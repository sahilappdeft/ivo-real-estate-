var formData = {
    "office-name": "",
    "office-purpose":""
}

function stateChange(key, value) {
    formData[key] = value
    console.log(formData, "formData")
}

accounts = []
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
    console.log(index, "index", key, "key", value, "value")
    accounts[index][key] = value
    console.log(accounts, "getAfterHyphen")
}

invite
function StateinviteEmployee(key, value){

}
