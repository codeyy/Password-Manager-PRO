// saved-password
    document.getElementById('sp_showpassword').addEventListener('click', function () {
        const sp_targetElement = document.getElementById('sp_main-pass-container');
        sp_targetElement.innerHTML = '';

        const form = document.createElement('form');
        form.setAttribute('method', 'POST');
        form.setAttribute('class', 'Pass_form');
        form.setAttribute('action', '/passwords');
        sp_targetElement.appendChild(form);

        const label = document.createElement('label');
        label.textContent = "Verify Your Password: ";
        label.setAttribute('class', 'pass-label');
        form.appendChild(label);

        form.appendChild(document.createElement('br'));
        form.appendChild(document.createElement('br'));

        const passwordInput = document.createElement('input');
        passwordInput.setAttribute('type', 'password');
        passwordInput.setAttribute('name', 'password');
        passwordInput.setAttribute('required', true);
        passwordInput.setAttribute('autofocus', true);
        passwordInput.setAttribute('placeholder', 'Password');
        passwordInput.setAttribute('class', 'form-input');
        form.appendChild(passwordInput);

        const br = document.createElement('br');
        form.appendChild(br);

        const submitButton = document.createElement('button');
        submitButton.setAttribute('type', 'submit');
        submitButton.setAttribute('class', 'form-button');
        submitButton.style.marginTop = "20px"
        submitButton.textContent = 'Submit';
        form.appendChild(submitButton);
    });
