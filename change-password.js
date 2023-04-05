//import zxcvbn from 'zxcvbn'
var users_url = "http://localhost:5000/";
var password_policy_url = "http://localhost:5001/";

// Check password strength using zxcvbn.js and update strength meter and text
var meter = document.getElementById('password-strength-meter');
var text = document.getElementById('password-strength-text');
var submitButton = document.getElementById("submit-button");
var passwordChangeForm = document.getElementById('pass-change-form')
var changePasswordInput = document.getElementById('new-password')
var params = new URLSearchParams(window.location.search);
var username = params.get("username");
var proceedButton = document.getElementById("proceed-button");

proceedButton.disabled = true;
proceedButton.addEventListener('click', redirectToHome);

function redirectToHome() {
    location.replace("templates/main.html");
}



// Disables submit button for registation form unless zxvbn condition is met
submitButton.disabled = true;

changePasswordInput.addEventListener('input', checkPasswordStrength);

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





passwordChangeForm.addEventListener("submit", changePassword);
function changePassword(event) {
    // Prevent the default form submission
    event.preventDefault();
    // Get the form data
    var current_password = document.getElementById("current-password").value;
    var new_password = document.getElementById("new-password").value;
    var re_new_password = document.getElementById("re-new-password").value;

    // Do something with the data
    // If current_password == new_password, return error
    if (current_password == new_password) {
        document.getElementById("response-message").innerHTML = "Please enter a different password from your current password";
        throw new Error('Current and new password cannot be the same');
    }

    // If new_password and re_new_password do not match, return error
    var data = {
        current_password: current_password,
        new_password: new_password,
        username: username
    }
    console.log(data)


    fetch(password_policy_url + "change_password", {
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
            document.getElementById("response-message").innerHTML = data["data"];
            if (data["code"] == 200) {
                proceedButton.disabled = false;
            }

        })
        .catch(error => {
            console.error('Error:', error);
        });

}


