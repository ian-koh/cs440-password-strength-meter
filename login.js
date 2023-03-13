//import zxcvbn from 'zxcvbn'
var password_policy_url = "http://localhost:5001/"

// Check password strength using zxcvbn.js and update strength meter and text
var usernameInput = document.getElementById('username-login');
var passwordInput = document.getElementById('password-login');
var loginForm = document.getElementById('login-form');



//onSubmitting login form, calls the backend to validate user to database with password hashed with bcrypt
loginForm.addEventListener("submit", processFormData);
async function processFormData(event) {
    // Get the form data
    var username = document.getElementById("username-login").value;
    var password = document.getElementById("password-login").value;

    // Do something with the data
    console.log(username);
    console.log(password);
    var data = {
        username: username,
        password: password
    }
    console.log(data)
    // Prevent the default form submission
    event.preventDefault();

    response = await fetch(password_policy_url + "login", {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    result = await response.json();
    if (result.code === 200) {
        window.location.replace("templates/main.html")
    }
    if (result.code === 401) {
        document.getElementById("error-message").innerHTML = "Unauthorized"
    }





}
