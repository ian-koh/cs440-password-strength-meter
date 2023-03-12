//import zxcvbn from 'zxcvbn'
var users_url = "http://localhost:5000/"

// Check password strength using zxcvbn.js and update strength meter and text
var usernameInput = document.getElementById('username_register')
var passwordInput = document.getElementById('password_register');
var meter = document.getElementById('password-strength-meter');
var text = document.getElementById('password-strength-text');
var submitButton = document.getElementById("submit-button");

passwordInput.addEventListener('input', function () {
    text.innerHTML = "hi"
    //check the password strength and return the result
    var result = zxcvbn(passwordInput.value);
    meter.value = result.score;
    if (passwordInput.value !== "") {
        submitButton.disabled = true;
        if (result.score == 4) {
            submitButton.disabled = false;
        }
        text.innerHTML = "Password strength: " + result.score + "/4 \n " + result.feedback.warning + " " + result.feedback.suggestions;
    } else {
        text.innerHTML = "";
    }
});


submitButton.addEventListener('click', function () {
    //On click submit, send to backend to hash the password with bcrypt
    var data = {
        username: usernameInput,
        password: passwordInput
    }
    console.log(data)
    fetch(users_url + "users", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error.');
            }
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

});

