// login
    const log_passwordInput = document.getElementById('log-password');
    const log_toggleButton = document.getElementById('toggle-log-Password');
    const log_submitButton = document.getElementById('log-submit');
    const log_usernameInput = document.getElementById('log-username');
    const log_passwordInputField = document.getElementById('log-password');

    log_toggleButton.addEventListener('click', function () {
        const type = log_passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        log_passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });
    
    log_submitButton.addEventListener('click', function (event) {
        if (log_usernameInput.value.trim() === '') {
            event.preventDefault(); // Prevent form submission
            log_usernameInput.style.border = '1px solid red';
        }
        if (log_passwordInputField.value.trim() === '') {
            event.preventDefault(); // Prevent form submission
            log_passwordInputField.style.border = '1px solid red';
        }
    });