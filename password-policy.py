from datetime import datetime, timedelta
from flask import Flask, request, redirect, render_template, jsonify, url_for
import bcrypt
import requests
from flask_cors import CORS
from invokes import invoke_http
import json


users_url = "http://localhost:5000/"
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# Set the password expiration time limit in days
PASSWORD_EXPIRATION_DAYS = 60


# Function to check if a user's password has expired
def is_password_expired(user):
    last_password_change_date = user["last_password_change_date"]
    expiration_date = datetime.strptime(
        last_password_change_date, "%Y-%m-%d"
    ) + timedelta(days=PASSWORD_EXPIRATION_DAYS)
    return datetime.now() > expiration_date


# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]
        print(username)
        print(password)
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        try:
            response = invoke_http(users_url + "users/" + username)
            user = json.loads(response["data"])
            print(type(user))
            print(user)

        except:
            return jsonify({"code": 500, "data": "User does not exist"})
        # If password is wrong
        if not bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        ):
            return jsonify({"code": 401, "data": "Incorrect password"}), 401
            # Check if the user's password has expired
        else:
            if is_password_expired(user):
                # Redirect the user to the change password page
                return redirect(url_for("change_password", username=username))

            return jsonify({"code": 200, "data": "Welcome " + username})
    return render_template("login.html")


# home page route
@app.route("/home")
def home():
    username = request.args.get("username")
    message = "Welcome " + str(username)
    return "Welcome " + username


# Route for changing the user's password
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    username = request.args.get("username")
    print(username)
    # Redirect the user to the login page
    if request.method == "POST":
        current_password = request.json["current_password"]
        new_password = request.json["new_password"]
        username = request.json["username"]
        # Prevent user from entering same password
        data = {
            "current_password": current_password,
            "new_password": new_password,
            "username": username,
        }
        print(data)
        try:
            result = invoke_http(
                users_url + "users/change_password",
                method="PUT",
                json=data,
                headers={"Content-Type": "application/json"},
            )
            return jsonify(
                {
                    "code": 200,
                    "data": "Password changed successfully",
                }
            )
        except:
            return jsonify({"code": 602, "data": "error"})
    return jsonify({"code": 600, "data": "Please change your password"})


if __name__ == "__main__":
    app.run(port=5001, debug=True)
