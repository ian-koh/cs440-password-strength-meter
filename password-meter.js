// Import the zxcvbn library
import zxcvbn from 'zxcvbn';

// Check password strength using zxcvbn.js and update strength meter and text
var passwordInput = document.getElementById('password');
var meter = document.getElementById('password-strength-meter');
var text = document.getElementById('password-strength-text');

passwordInput.addEventListener('input', function () {
    var result = zxcvbn(passwordInput.value);
    meter.value = result.score;
    if (passwordInput.value !== "") {
        text.innerHTML = "Password strength: " + result.score + "/4 - " + result.feedback.warning;
    } else {
        text.innerHTML = "";
    }
});

// Define a function to check the password strength and return the result
function checkPasswordStrength(password) {
    return zxcvbn(password);
}

// Define a function to prompt the user to enter a password and return the result
function promptForPassword() {
    const password = prompt('Enter a password:');
    return zxcvbn(password);
}

// Define a function to generate suggestions for improving the password
function generatePasswordSuggestions(result) {
    const suggestions = [];

    if (result.feedback.warning) {
        suggestions.push(result.feedback.warning);
    }

    if (result.feedback.suggestions.length > 0) {
        suggestions.push(...result.feedback.suggestions);
    }

    return suggestions;
}

// Example usage
const result = promptForPassword();
console.log(`Password strength: ${result.score}`);
console.log(`Suggestions: ${generatePasswordSuggestions(result).join(', ')}`);
