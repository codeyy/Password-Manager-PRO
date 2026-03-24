// veri-hash-password
    const vh_passwordInput         = document.getElementById('vh_check_password');
    const vh_toggleButton          = document.getElementById('vh_toggle_Password');
    const vh_hashInputField        = document.querySelector('#vh_hash');
    const vh_algoInputField        = document.getElementById("vh_algorithm");
    const vh_submitButton          = document.querySelector('#vh_submitButton');
    
    const vh_hiddenInputField      = document.getElementById("vh_hdn_algorithm");
    const vh_dropdown              = document.getElementById("vh_dropdown");
    const vh_opt1                  = document.getElementById("vh_opt1");
    const vh_opt2                  = document.getElementById("vh_opt2");
    const vh_opt3                  = document.getElementById("vh_opt3");
    const vh_opt4                  = document.getElementById("vh_opt4");
    
    vh_toggleButton.addEventListener('click', function () {
        const type = vh_passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        vh_passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });


    vh_submitButton.addEventListener('click', function (event) {
        if (vh_passwordInput.value.trim() === '') {
            event.preventDefault();
            vh_passwordInput.style.border = '1px solid red';
        }else{vh_passwordInput.style.border = '';}
        if (vh_hashInputField.value.trim() === '') {
            event.preventDefault();
            vh_hashInputField.style.border = '1px solid red';
        }else{vh_hashInputField.style.border = '';}
        if (vh_hiddenInputField.value === '') {
            event.preventDefault();
            vh_algoInputField.style.border = '1px solid red';
        }else{vh_algoInputField.style.border = '';}
        
    });

    vh_opt1.addEventListener('click', function() {
        vh_hiddenInputField.value = vh_opt1.textContent;
        vh_algoInputField.textContent = vh_opt1.textContent;
        vh_dropdown.style.display = "none";
        setTimeout(() => {
        vh_dropdown.style.display = ""; 
        }, 100); 
    })
    vh_opt2.addEventListener('click', function() {
        vh_hiddenInputField.value = vh_opt2.textContent;
        vh_algoInputField.textContent = vh_opt2.textContent;
        vh_dropdown.style.display = "none";
        setTimeout(() => {
        vh_dropdown.style.display = ""; 
        }, 100);
    })
    vh_opt3.addEventListener('click', function() {
        vh_hiddenInputField.value = vh_opt3.textContent;
        vh_algoInputField.textContent = vh_opt3.textContent;
        vh_dropdown.style.display = "none";
        setTimeout(() => {
        vh_dropdown.style.display = ""; 
        }, 100);
    })
    vh_opt4.addEventListener('click', function() {
        vh_hiddenInputField.value = vh_opt4.textContent;
        vh_algoInputField.textContent = vh_opt4.textContent;
        vh_dropdown.style.display = "none";
        setTimeout(() => {
        vh_dropdown.style.display = ""; 
        }, 100);
    })