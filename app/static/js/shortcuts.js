  
  document.addEventListener('keydown', function(event) {
    // Check if Ctrl key is pressed
    const isCtrlPressed = event.ctrlKey || event.metaKey;

    // Check if Shift key is pressed
    const isShiftPressed = event.shiftKey;

    if (isCtrlPressed  && (event.key === 'h' || event.key === 'H')) {
        event.preventDefault();
        window.location.href = "/"
    }
    if (isCtrlPressed && isShiftPressed && event.key === ' ') {
        event.preventDefault(); 
        window.location.href = "/logout"
    }
    if (isCtrlPressed && (event.key === 'q' || event.key === 'Q')) {
        event.preventDefault(); 
        window.location.href = "/add-password"
    }
    if (isCtrlPressed && isShiftPressed && (event.key === 'q' || event.key === 'Q')) {
        event.preventDefault(); 
        window.location.href = "/del-password"
    }
    if (isCtrlPressed && (event.key === 'z' || event.key === 'Z')) {
        event.preventDefault(); 
        window.location.href = "/passwords_strength"
    }
    if (isCtrlPressed && (event.key === 'd' || event.key === 'D')) {
        event.preventDefault(); 
        window.location.href = "/hash_password"
    }
    if (isCtrlPressed && isShiftPressed && (event.key === 'd' || event.key === 'D')) {
        event.preventDefault(); 
        window.location.href = "/verifyHash"
    }
    if (isCtrlPressed  && (event.key === 's' || event.key === 'S')) {
        event.preventDefault(); 
        window.location.href = "/passwords"
    }
    if ((event.ctrlKey || event.metaKey) && (event.key === '?' || event.key === '/')) {
        event.preventDefault();
        showInstructionPopup();
    }
});