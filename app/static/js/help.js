  document.getElementById("helper_key").addEventListener('click', function(event) {
    showInstructionPopup()
});

function showInstructionPopup() {
    // Check if popup already exists, remove it
    if (document.getElementById('help-popup')) {
        document.getElementById('help-popup').remove();
        return;
    }

    // Create the popup container
    const popup = document.createElement('div');
    popup.id = 'help-popup';
    popup.classList.add('glassmorphicpopup')

    // Populate with instructions
    
    popup.innerHTML = `<h1>Help</h1>

<p>
This application is a secure password manager designed to help you store and manage
credentials safely. Passwords are encrypted using a key derived from your
<strong>master password</strong>, ensuring that only you can access your stored data.
The system also includes tools for analyzing password strength and working with
secure password hashes.
</p>

<h2>Services</h2>

<ul>
  <li>
    <strong>Add Password</strong><br>
    Store credentials for a service securely in your encrypted vault.
  </li>
  <br>
  <li>
    <strong>Delete Password</strong><br>
    Remove stored credentials from the vault when they are no longer needed.
  </li>
  <br>
  <li>
    <strong>Check Password Strength</strong><br>
    Analyze a password to evaluate its strength based on length, complexity,
    and character diversity.
  </li>
  <br>
  <li>
    <strong>Hash Password</strong><br>
    Generate a secure cryptographic hash of a password for safe storage or verification.
  </li>
  <br>
  <li>
    <strong>Verify Hash</strong><br>
    Check whether a password matches a previously generated hash.
  </li>
</ul>

<h2>Keyboard Shortcuts</h2>

<ul class="shortcut-list">
  <li><span class="shortcut-label"><strong>Open Help</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + ?</span></li>
  <li><span class="shortcut-label"><strong>Home</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + h</span></li>
  <li><span class="shortcut-label"><strong>Saved Passwords</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + S</span></li>
  <li><span class="shortcut-label"><strong>Add Password</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + Q</span></li>
  <li><span class="shortcut-label"><strong>Check Password Strength</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + Z</span></li>
  <li><span class="shortcut-label"><strong>Hash Password</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + D</span></li>
  <li><span class="shortcut-label"><strong>Verify Hash</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + Shift + D</span></li>
  <li><span class="shortcut-label"><strong>Delete Password</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + Shift + Q</span></li>
  <li><span class="shortcut-label"><strong>Fast LogOut</strong></span><span class="shortcut-key" style="text-align: center;">Ctrl + Shift + Space</span></li>
</ul>
<style>
.shortcut-list {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  max-width: 400px;
}
.shortcut-list li {
  display: flex;
  border: none;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0,0,0,0.07);
}
.shortcut-label {
  flex: 1;
  text-align: left;
}
.shortcut-key {
  min-width: 140px;
  text-align: right;
  font-weight: bold;
}
</style>
</ul>
<br>
<button id="close-popup" class="form-button" title="ctrl+h";
">Close</button>`

    // Add to body
    document.body.appendChild(popup);
    
    document.getElementById('close-popup').addEventListener('click', () => {
        popup.remove();
    });
}