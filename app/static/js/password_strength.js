    // password-strength
    const ps_passin       = document.getElementById('ps_check_password')
    const ps_progressBar  = document.getElementById('ps-progressBar')
    const ps_crackTime    = document.getElementById('ps_crackTime')
    const ps_entropy      = document.getElementById('ps_entropy')
    const ps_glass_shell  = document.getElementById('ps_glass_shell')
    const ps_toggleButton = document.getElementById('ps-toggle-Password');
    

    ps_toggleButton.addEventListener('click', function () {
        const type = ps_passin.getAttribute('type') === 'password' ? 'text' : 'password';
        ps_passin.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Show' : 'Hide';
    });


    ps_passin.addEventListener('input', function(){
        if (ps_passin.value === "") {
            ps_crackTime.textContent = ""
            ps_entropy.textContent = ""
            ps_glass_shell.classList = ""
            return
        }
        ps_glass_shell.classList = "glassmorphicHints"
        fetch('/api/passwords_strength', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: ps_passin.value })
        })
        .then(response => response.json())
        .then(data => {
            ps_progressBar.style.width = `${data.time_score}%`;
            ps_progressBar.textContent = `${data.time_score}%`;
            ps_progressBar.style.backgroundColor = percentageToColorSpectrum(data.time_score, false)
            ps_progressBar.style.color = percentageToColorSpectrum(data.time_score, true)
            
            ps_entropy.textContent = `Entropy---${data.entropy}`;
            ps_crackTime.textContent = `Estimated time to crack---${data.est_time}`;
            ps_entropy.style.color = percentageToColorSpectrum(data.time_score, false)
            ps_crackTime.style.color = percentageToColorSpectrum(data.time_score, false)
            
        })
        .catch((error) => {
            // Handle any errors
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