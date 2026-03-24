// add-password
    const ap_passwordInput = document.getElementById('add-password');
    const ap_toggleButton = document.getElementById('add-toggle-Password');
    const ap_submitbutton = document.getElementById('ap_submitbutton');
    const ap_category = document.getElementById('add-category');

    ap_toggleButton.addEventListener('click', function () {
        const type = ap_passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        ap_passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });
    
    ap_form.addEventListener('submit', function (event) {
        if (ap_passwordInput.value === '') {
            event.preventDefault();
            ap_passwordInput.style.border = '1px solid red';
        }
        if (ap_hiddenInputField.value === '') {
            event.preventDefault();
            ap_hiddenInputField.style.border = '1px solid red';
        }
        if (ap_category.value === '') {
            ap_category.value = 'N/A';
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

