// del-password
    const del_passwordInput = document.getElementById('del-master_password');
    const del_toggleButton = document.getElementById('del-toggle-Password');

    del_toggleButton.addEventListener('click', function () {
        const type = del_passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        del_passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });