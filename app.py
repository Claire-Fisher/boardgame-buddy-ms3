import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__, static_url_path='/static')

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/library")
def library():
    games = list(mongo.db.games.find())
    return render_template("library.html", games=games)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "city": "",
            "country": "",
            "favourite_game": ""
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            # ensure hashed password matched user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # creates a list of session user's data
    info = mongo.db.users.find_one({"username": username})

    if session["user"]:
        return render_template("profile.html", info=info)

    return redirect(url_for("login"))


@app.route("/edit_profile/<username>", methods=["GET", "POST"])
def edit_profile(username, placeholder=None):
    info = mongo.db.users.find_one({"username": username})
    # placeholder instructions for user if values are blank
    placeholder = {
        "city": "Enter your City here" if info["city"] == "" else "",
        "country": "Enter your Country here" if info["country"] == "" else "",
        "favourite_game": "Enter your Favourite Game here" if info["favourite_game"] == "" else ""
    }

    if request.method == "POST":
        save = {
            "city": request.form.get("city"),
            "country": request.form.get("country"),
            "favourite_game": request.form.get("favourite_game")
        }
        # find the object id
        match_id = {"_id": info["_id"]}
        # set save object data to the matched user
        mongo.db.users.update_one(match_id, {"$set": save})
        # redirect back to updated user profile page
        flash("Profile Successfully Updated")
        return redirect(url_for("profile", username=username))
    return render_template("edit_profile.html", info=info, placeholder=placeholder)


@app.route("/delete_profile/<user_id>")
def delete_profile(user_id):
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    session.pop("user")
    flash("Profile Successfully Deleted")
    return redirect(url_for("index"))


@app.route("/game/<game_id>", methods=["GET"])
def game_detail(game_id):
    print(game_id)

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    print(game)

    return redirect(url_for("library"))


@app.route("/logout")
def logout():
    # remove user from the session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
