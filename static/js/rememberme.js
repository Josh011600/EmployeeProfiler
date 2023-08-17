// Check if the "Remember Me" checkbox is checked on page load
window.addEventListener('load', function() {
    const rememberMeCheckbox = document.getElementById('rememberMe');
    const storedUsername = localStorage.getItem('rememberedUsername');

    if (rememberMeCheckbox && storedUsername) {
        document.getElementById('username').value = storedUsername;
        rememberMeCheckbox.checked = true;
    }
});

// Save the username in localStorage if "Remember Me" is checked
document.getElementById('rememberMe').addEventListener('change', function() {
    const rememberMeCheckbox = document.getElementById('rememberMe');
    const usernameField = document.getElementById('username');
    
    if (rememberMeCheckbox.checked) {
        localStorage.setItem('rememberedUsername', usernameField.value);
    } else {
        localStorage.removeItem('rememberedUsername');
    }
});
