// Import the zxcvbn library
import zxcvbn from 'zxcvbn';

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
