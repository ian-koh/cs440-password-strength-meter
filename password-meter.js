
var users_url = "http://localhost:5000/";
// var password_policy_url = "http://localhost:5001/";

// Check password strength using zxcvbn.js and update strength meter and text
var usernameInput = document.getElementById('username-register');
var passwordInput = document.getElementById('password-register');
var meter = document.getElementById('password-strength-meter');
var text = document.getElementById('password-strength-text');
var submitButton = document.getElementById("submit-button");
var regForm = document.getElementById('reg-form');





// Disables submit button for registation form unless zxvbn condition is met
submitButton.disabled = true;

passwordInput.addEventListener('input', checkPasswordStrength);

function checkPasswordStrength() {
    //check the password strength and return the result
    var result = zxcvbn(this.value);
    meter.value = result.score;
    if (this.value !== "") {
        submitButton.disabled = true;
        if (result.score == 4) {
            submitButton.disabled = false;
        }
        text.innerHTML = "Password strength: " + result.score + "/4 \n " + result.feedback.warning + " " + result.feedback.suggestions;
    } else {
        text.innerHTML = "";
    }
}

//onSubmitting registration form, calls the backend and add user to database with password hashed with bcrypt
regForm.addEventListener("submit", registerUser);
function registerUser(event) {
    // Prevent the default form submission
    event.preventDefault();
    // Get the form data
    var username = document.getElementById("username-register").value;
    var password = document.getElementById("password-register").value;

    // Do something with the data
    console.log(username);
    console.log(password);
    var data = {
        username: username,
        password: password
    }
    console.log(data)


    fetch(users_url + "users", {
        method: 'POST',
        mode: 'cors',
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
            document.getElementById("response-message").innerHTML = data["message"];
        })
        .catch(error => {
            console.error('Error:', error);
        });

}
