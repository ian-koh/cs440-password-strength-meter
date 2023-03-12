from flask import Flask, request
import bcrypt

app = Flask(__name__)


@app.route("/hash_password", methods=["POST"])
def hash_password():
    # Get the password from the request
    password = request.json.get("password")

    # Generate a salt to use in the hash
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Return the hashed password as a JSON response
    return {"hashed_password": hashed_password.decode("utf-8")}


if __name__ == "__main__":
    app.run(debug=True)
