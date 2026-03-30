// del-password
    const dp_service = document.getElementById('del-service');
    const dp_usernameInput = document.getElementById('del-username');
    const dp_MasterPasswordInputField = document.getElementById('del-master_password'); 
    const dp_toggleButton = document.getElementById('del-toggle-Password'); 
    const dp_submitbutton = document.getElementById('del-submitbutton');

    dp_toggleButton.addEventListener('click', function () {
        const type = dp_MasterPasswordInputField.getAttribute('type') === 'password' ? 'text' : 'password';
        dp_MasterPasswordInputField.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });

    dp_submitbutton.addEventListener('click', function (event) {
        if (dp_service.value.trim() === '') {
            event.preventDefault();
            dp_service.style.border = '1px solid red';
        }
        if (dp_usernameInput.value.trim() === '') {
            event.preventDefault();
            dp_usernameInput.style.border = '1px solid red';
        }
        if (dp_MasterPasswordInputField.value === '') {
            event.preventDefault();
            dp_MasterPasswordInputField.style.border = '1px solid red';
        }
    });