// hash-password
    const hp_passwordInput         = document.getElementById('hp_password');
    const hp_toggleButton          = document.getElementById('hp_toggle-Password');
    const hp_submitButton          = document.getElementById('hp_submitButton');
    const hp_algoInputField        = document.getElementById("hp_algorithm");

    const hp_hiddenInputField      = document.getElementById("hp_hdn_algorithm");
    const hp_dropdown              = document.getElementById("hp_dropdown");
    const hp_opt1                  = document.getElementById("hp_opt1");
    const hp_opt2                  = document.getElementById("hp_opt2");
    const hp_opt3                  = document.getElementById("hp_opt3");
    const hp_opt4                  = document.getElementById("hp_opt4");
  
    hp_toggleButton.addEventListener('click', function () {
        const type = hp_passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        hp_passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });

    hp_submitButton.addEventListener('click', function (event) {
        if (hp_passwordInput.value.trim() === '') {
            event.preventDefault();
            hp_passwordInput.style.border = '1px solid red';
        }else{hp_passwordInput.style.border = '';}
        if (hp_hashInputField.value.trim() === '') {
            event.preventDefault();
            hp_hashInputField.style.border = '1px solid red';
        }else{hp_hashInputField.style.border = '';}
        if (hp_hiddenInputField.value === '') {
            event.preventDefault();
            hp_algoInputField.style.border = '1px solid red';
        }else{hp_algoInputField.style.border = '';}
    });
    
    hp_opt1.addEventListener('click', function() {
        hp_hiddenInputField.value = hp_opt1.textContent;
        hp_algoInputField.textContent = hp_opt1.textContent;
        hp_dropdown.style.display = "none";
        setTimeout(() => {
        hp_dropdown.style.display = ""; 
        }, 100); 
    })
    hp_opt2.addEventListener('click', function() {
        hp_hiddenInputField.value = hp_opt2.textContent;
        hp_algoInputField.textContent = hp_opt2.textContent;
        hp_dropdown.style.display = "none";
        setTimeout(() => {
        hp_dropdown.style.display = ""; 
        }, 100);
    })
    hp_opt3.addEventListener('click', function() {
        hp_hiddenInputField.value = hp_opt3.textContent;
        hp_algoInputField.textContent = hp_opt3.textContent;
        hp_dropdown.style.display = "none";
        setTimeout(() => {
        hp_dropdown.style.display = ""; 
        }, 100);
    })
    hp_opt4.addEventListener('click', function() {
        hp_hiddenInputField.value = hp_opt4.textContent;
        hp_algoInputField.textContent = hp_opt4.textContent;
        hp_dropdown.style.display = "none";
        setTimeout(() => {
        hp_dropdown.style.display = ""; 
        }, 100);
    })