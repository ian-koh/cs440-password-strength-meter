from datetime import datetime, timedelta
from flask import Flask, request, redirect, render_template

users_url = "http://localhost:5000/"
app = Flask(__name__)

# Set the password expiration time limit in days
PASSWORD_EXPIRATION_DAYS = 60


# Function to check if a user's password has expired
def is_password_expired(user):
    last_password_change_date = user.last_password_change_date
    expiration_date = last_password_change_date + timedelta(
        days=PASSWORD_EXPIRATION_DAYS
    )
    return datetime.now() > expiration_date


# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if the user's password has expired
        user = users_url + "/users/" + (request.form["username"])
        if user and is_password_expired(user):
            # Redirect the user to the change password page
            return redirect("/change_password")
        # Check the user's login credentials and log them in
        # ...
    else:
        return render_template("login.html")


# Route for changing the user's password
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        # Update the user's password in the database
        # Update the user's last_password_change_date to the current date
        user = users_url + "/users/" + (request.form["username"])
        # Redirect the user to the login page
        return redirect("/login")
    else:
        return render_template("change_password.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
