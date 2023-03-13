from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import datetime
from flask_cors import CORS
import json
from datetime import date

# General flask settings
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root@localhost:3306/users"
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# Instantiate db model for users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_password_change_date = db.Column(db.Date, nullable=False)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        return super().default(obj)


def model_to_json(model_obj):
    return json.dumps(
        {
            column.name: getattr(model_obj, column.name)
            for column in model_obj.__table__.columns
        },
        cls=CustomEncoder,
    )


# Update user password endpoint for when password expires after 60 days
@app.route("/users/<username>/password", methods=["PUT"])
def update_user_password(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        return {"message": "User not found"}, 404

    current_password = request.json["current_password"]
    new_password = request.json["new_password"]
    if not bcrypt.checkpw(
        current_password.encode("utf-8"), user.password_hash.encode("utf-8")
    ):
        return {"message": "Incorrect password"}, 401

    new_hashed_password = bcrypt.hashpw(
        new_password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    user.password_hash = new_hashed_password
    user.last_password_change_date = datetime.date.today()
    db.session.commit()

    return {"message": "Password updated successfully"}


# ----------------------------------------------REGISTRATION -----------------------------------------------------------


# Creates user and stores zxcvbn password as bcrypt hashed password
@app.route("/users", methods=["POST"])
def create_user():
    username = request.json["username"]
    password = request.json["password"]
    print(username)
    print(password)
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    new_user = Users(
        username=username,
        password_hash=hashed_password,
        last_password_change_date=datetime.date.today(),
    )

    try:
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        print("\n Error in committing to database")
        print(e)

        return (
            jsonify(
                {
                    "code": 500,
                    "data": {"username": new_user["username"]},
                    "message": "An error occurred when creating the new user",
                }
            ),
            500,
        )

    return {"message": "User created successfully"}


# ------------------------------------------------------------------------------------LOGIN-------------------------------------------------------------------------------------


# Get all users
@app.route("/users")
def get_users():
    users = Users.query.all()
    return {"users": [user.username for user in users]}


# Get user by username
@app.route("/users/<username>")
def get_user_by_username(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    else:
        print(user.password_hash)
        return jsonify({"code": 200, "data": model_to_json(user)}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
