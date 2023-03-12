from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return f"User {username} created with id {user.id}"



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
