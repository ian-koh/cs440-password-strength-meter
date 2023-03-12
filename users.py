from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/users"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_password_change_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


# Creates user and stores zxcvbn password as bcrypt
@app.route("/users", methods=["POST"])
def create_user():
    username = request.json["username"]
    password = request.json["password"]
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    new_user = User(
        username=username,
        password_hash=hashed_password,
        last_password_change_date=datetime.date.today(),
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully"}


@app.route("/users/<username>/password", methods=["PUT"])
def update_user_password(username):
    user = User.query.filter_by(username=username).first()
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


@app.route("/users")
def get_users():
    users = User.query.all()
    return {"users": [user.username for user in users]}


@app.route("/users/<username>")
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {"message": "User not found"}, 404
    else:
        return {
            "username": user.username,
            "last_password_change_date": user.last_password_change_date,
        }


if __name__ == "__main__":
    app.run(port=5000, debug=True)
