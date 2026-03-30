// add-password
    const ap_service = document.getElementById('add-service');
    const ap_passwordInputField = document.getElementById('add-password');
    const ap_usernameInput = document.getElementById('add-username');
    const ap_MasterPasswordInputField = document.getElementById('add-master_password');
    const ap_submitbutton = document.getElementById('ap_submitbutton');

    document.getElementById('add-toggle-Password').addEventListener('click', function () {
        const type = ap_passwordInputField.getAttribute('type') === 'password' ? 'text' : 'password';
        ap_passwordInputField.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });
    
    ap_submitbutton.addEventListener('click', function (event) {
        if (ap_service.value.trim() === '') {
            event.preventDefault();
            ap_service.style.border = '1px solid red';
        }
        if (ap_usernameInput.value.trim() === '') {
            event.preventDefault();
            ap_usernameInput.style.border = '1px solid red';
        }
        if (ap_passwordInputField.value.trim() === '') {
            event.preventDefault();
            ap_passwordInputField.style.border = '1px solid red';
        }
        if (ap_MasterPasswordInputField.value === '') {
            event.preventDefault();
            ap_MasterPasswordInputField.style.border = '1px solid red';
        }
    });
    
    function updateValue() {
    // Access the input element using its name property or document.getElementById
    if (document.ap_form.category.value === ""){
        document.ap_form.category.value = "N/A";
    }
    // Return true to allow the form to submit
    return true;
}

