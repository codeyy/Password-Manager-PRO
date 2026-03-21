// register
    // Toggle password visibility
    const passwordInput = document.getElementById('reg-password');
    const toggleButton = document.getElementById('toggle-reg-Password');
    toggleButton.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });
    const submitButton = document.querySelector('#reg-button');
    const usernameInput = document.querySelector('#reg-username');
    const passwordInputField = document.querySelector('#reg-password');
    const rePasswordInputField = document.querySelector('#re-reg-password');
    const progressBar = document.getElementById('progressBar');

    let curr_pass_stren = 0;
    let good_pass_stren = 60;

    // Form validation
    submitButton.addEventListener('click', function (event) {
        if (usernameInput.value.trim() === '') {
            event.preventDefault();
            usernameInput.style.border = '1px solid red';
        }
        if (passwordInputField.value.trim() === '') {
            event.preventDefault();
            passwordInputField.style.border = '1px solid red';
        } else if (curr_pass_stren < good_pass_stren && passwordInputField.value.length < 10) {
            event.preventDefault();
            alert("Weak Password \n(please setup a stronger password as its vital for your vault)");
        }
        if (rePasswordInputField.value.trim() === '') {
            event.preventDefault();
            rePasswordInputField.style.border = '1px solid red';
        }
        if (rePasswordInputField.value != passwordInputField.value) {
            event.preventDefault();
            rePasswordInputField.style.border = '1px solid red';
        }
    });

    // Password strength bar
    passwordInputField.addEventListener('input', function () {
        fetch('/api/passwords_strength', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: passwordInputField.value })
        })
        .then(response => response.json())
        .then(data => {
            progressBar.style.width = `${data.time_score}%`;
            progressBar.textContent = `${data.time_score}%`;
            progressBar.style.backgroundColor = percentageToColorSpectrum(data.time_score, false)
            progressBar.style.color = percentageToColorSpectrum(data.time_score, true)
            curr_pass_stren = `${data.time_score}%`;
        })
        .catch(error => {
            console.error('Error:', error);
        });

        function percentageToColorSpectrum(percentage, invert=false) {
        // or a specific range like -30 to 295 (red to bark blue-purpleish) as often used for status indicators.
        const hue = (percentage / 100) * 290; 
              
        // Set saturation and lightness to a constant value for a vivid color
        const saturation = '100%';
        const lightness = '50%'; // 50% lightness avoids black (0%) or white (100%)
        if (invert == true){return `hsl(${hue + 180}, ${saturation}, ${lightness})`}
        return `hsl(${hue-30}, ${saturation}, ${lightness})`;
        }
    });

    // Re-enter password validation
    rePasswordInputField.addEventListener('input', function () {
        if (rePasswordInputField.value !== passwordInputField.value) {
            rePasswordInputField.style.border = '1px solid red';
        } else {
            rePasswordInputField.style.border = '';
        }
    });

    // Username existence check
    usernameInput.addEventListener("input", function () {
        const words = "This Username Already Exists";
        fetch("/api/checkUsername", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: usernameInput.value })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                usernameInput.style.border = '1px solid red';
                if (!document.getElementById("userexisterror")) {
                    submitButton.type = "button"
                    let dist = 50;
                    for (const word of words) {
                        const snowflake = document.createElement('div');
                        snowflake.id = "userexisterror";
                        snowflake.classList.add('facyErrorSnowflake');
                        snowflake.textContent = word;
                        snowflake.style.left = dist + "vw";
                        snowflake.style.zIndex = 1;
                        snowflake.style.animationDuration = "10s";
                        snowflake.style.animationDelay = (Math.random() * (0.1 - 0.01) + 0.01) + "s";
                        snowflake.style.fontSize = "18px";
                        snowflake.style.color = "red";
                        snowflake.style.opacity = 1;
                        document.body.appendChild(snowflake);
                        dist += 1.1;
                    }
                }
            } else {
                submitButton.type = "submit";
                usernameInput.style.border = '';
                if (document.getElementById("userexisterror")) {
                    delayedLoop('userexisterror');
                }
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                }
                async function delayedLoop(idd) {
                    for (let i = 0; i < 28; i++) {
                        await sleep(20);
                        document.getElementById(idd)?.remove();
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
