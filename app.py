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
            "favourite_game": "",
            "avatar_url": "https://cdn1.iconfinder.com/data/icons/project-management-8/500/worker-512.png"
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
                existing_user["password"], request.form.get("password")
            ):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                print(session['user'])
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
    # grab the session user's username from the db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    info = mongo.db.users.find_one({"username": username})

    # gets the users profile avatar url and turns it into a string
    avatar = info.get("avatar_url")
    avatar = str(avatar)
    print(avatar)
    return render_template("profile.html", user=username, info=info, avatar=avatar)


@app.route("/edit_profile/<username>", methods=["GET", "POST"])
def edit_profile(username, placeholder=None):
    info = mongo.db.users.find_one({"username": username})
    # placeholder instructions for user if values are blank
    placeholder = {
        "city": "Enter your City here" if info["city"] == "" else "",
        "country": "Enter your Country here" if info["country"] == "" else "",
        "favourite_game": "Enter your Favourite Game here" if info["favourite_game"] == "" else ""
    }
    # gets the users profile avatar url and turns it into a string
    avatar = info.get("avatar_url")
    avatar = str(avatar)

    if request.method == "POST":
        save = {
            "city": request.form.get("city").lower(),
            "country": request.form.get("country").lower(),
            "favourite_game": request.form.get("favourite_game").lower(),
            "avatar_url": request.form.get("avatar_url")
        }
        # find the object id
        match_id = {"_id": info["_id"]}
        # set save object data to the matched user
        mongo.db.users.update_one(match_id, {"$set": save})
        # redirect back to updated user profile page
        flash("Profile Successfully Updated")
        return redirect(url_for("profile", username=username))
    return render_template("edit_profile.html", info=info, placeholder=placeholder, avatar=avatar)



@app.route("/game/<game_id>", methods=["GET", "POST"])
def game(game_id):
    """_summary_  Displays full info for a game selected by the user.

    Args:
        game_id (_str_): Game ObjectId

    Returns:
        _data_: displays full game info and all it's user reviews
    """
    # Finds all the data for the selected game
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    # Finds the username for the current session user
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    # Creates a list of all the review obj for the target game
    relevant_reviews = list(mongo.db.reviews.find({"game_id": game_id}))

    # Creates a new review obj from user input into the modal form
    if request.method == "POST":
        new_review = {
            "game_id": game_id,
            "game_title": game["game_title"],
            "review": request.form.get("review"),
            "review_title": request.form.get("review-title"),
            "username": username,
        }
        # Adds the new review obj to the db
        mongo.db.reviews.insert_one(new_review)
        # Adds the new review to the end of the relevant reviews list
        relevant_reviews.append(new_review)

    return render_template(
        "game.html", game=game, relevant_reviews=relevant_reviews)


@app.route("/collection/<game_id>", methods=["GET", "POST"])
def collection(game_id):
    """_summary_ Allows user to add a game to their personal collection.
    If all the conditions are met.

    Args:
        game_id (_str_): Game ObjectId

    Returns:
        _page_: refreshed render page. DB updates, if conditions met.
    """
    # Identifu the current game obj
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    # Finds the user obj for the current session user
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    # Finds the username for the current session user
    username = user["username"]
    # check if user collection exists in db
    existing_collection = mongo.db.collections.find_one(
            {"username": user["username"]})

    # Attempt to add game to user collection.
    if request.method == "POST":
        # Checks if the user has an existing collection
        if existing_collection:
            # Checks if the current game exists in user_collection arr
            if str(game["_id"]) in existing_collection["user_collection"]:
                flash("You already have this game in your collection.")
            else:
                # Adds game Id string to user_collection arr
                mongo.db.collections.update_one(
                    existing_collection,
                    {"$push": { "user_collection": str(game["_id"]) }})
        else:
            # Creates a new collection for the user
            new_collection = {
                "user_id": str(user["_id"]),
                "username": username,
                "user_collection": [game_id]
            }
            mongo.db.collections.insert_one(new_collection)

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
