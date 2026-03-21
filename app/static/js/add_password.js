// add-password
    const add_passwordInput = document.getElementById('add-password');
    const add_toggleButton = document.getElementById('add-toggle-Password');

    add_toggleButton.addEventListener('click', function () {
        const type = add_passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        add_passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });
