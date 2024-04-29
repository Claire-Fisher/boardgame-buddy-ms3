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


@app.route("/search", methods=["GET", "POST"])
def search():
    query = {}

    players = request.form.get('players')
    if not players:
        pass
    else:
        players = int(players)
        query["min_players"] = {"$lte": players}
        query["max_players"] = {"$gte": players}
        games = list(mongo.db.games.find(query))

    duration = request.form.get('duration')
    if not duration:
        pass
    else:
        duration = int(duration)
        query["avg_playtime_mins"] = {"$lte": duration}
        games = list(mongo.db.games.find(query))

    difficulty = request.form.get('difficulty')
    if not difficulty:
        pass
    else:
        query["difficulty"] = difficulty
        games = list(mongo.db.games.find(query))

    search = request.form.get("search")
    if not search:
        pass
    else:
        query["$text"] = {"$search": search}
        games = list(mongo.db.games.find(query))

    print(query)

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
            "avatar_url":
                "https://cdn1.iconfinder.com/data/icons/project-management-8/"
                "500/worker-512.png"
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        """ Calls new_collection() to generate an empty 
        collection for the new user"""
        new_collection(session["user"])
        flash("Registration Successful!")
        return redirect(url_for("library"))

    return render_template("register.html")


@app.route("/new_collection/<username>", methods=["POST"])
def new_collection(username):
    user = mongo.db.users.find_one({"username": username})

    create_collection = {
        "user_id": str(user["_id"]),
        "username": user["username"],
        "user_collection": [],
    }
    mongo.db.collections.insert_one(create_collection)

    return redirect(url_for("library"))


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
    # print()
    # print(avatar)
    collectionObj = mongo.db.collections.find_one(
        {"user_id": str(info["_id"])})
    # print(collectionObj)
    collection = collectionObj["user_collection"]
    # print(collection)

    collectionImages = []
    for game_id in collection:
        game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
        tuple = game["image"], game["game_title"], game_id
        collectionImages.append(tuple)

    return render_template(
        "profile.html",
        user=username,
        info=info,
        avatar=avatar,
        collectionImages=collectionImages)


@app.route("/edit_collection/<this_game>", methods=["GET", "POST"])
def edit_collection(this_game):
    """_summary_  Delete functionality.
    Gets the user collection games.
    User can remove games from their collection.

    Args:
        game_id (_str_): Game ObjectId

    Returns:
        _data_: refreshs profile page with deleted game instantly removed. 
    """
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    # gets the username
    username = user["username"]
    user_collection = mongo.db.collections.find_one(
        {"user_id": str(user["_id"])})
    target_game = mongo.db.games.find_one({"game_title": this_game})
    target_game_id = str(target_game["_id"])
    # Removes the game from the collections list and updates the db
    mongo.db.collections.update_one(
        {"_id": user_collection["_id"]},
        {"$pull": {"user_collection": target_game_id}}
    )

    flash("Game successfully removed from your collection")

    return redirect(url_for("profile", username=username))


@app.route("/edit_profile/<username>", methods=["GET", "POST"])
def edit_profile(username, placeholder=None):
    info = mongo.db.users.find_one({"username": username})
    # placeholder instructions for user if values are blank
    placeholder = {
        "city": "Enter your City here" if info["city"] == "" else "",
        "country": "Enter your Country here" if info["country"] == "" else "",
        "favourite_game":
            "Enter your Favourite Game here"
            if info["favourite_game"] == "" else ""
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
    return render_template(
        "edit_profile.html", info=info, placeholder=placeholder, avatar=avatar)



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
    # Creates a list of all the review obj for the target game
    relevant_reviews = list(mongo.db.reviews.find({"game_id": game_id}))
    # Check if a user is logged in
    username = None
    if "user" in session:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
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


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        # check if game already exists in db
        existing_game = mongo.db.games.find_one(
            {"game_title": request.form.get("game_title").lower()})

        if existing_game:
            flash("That game already exists")
            return redirect(url_for("add_game"))

        min_players = int(request.form.get("min_players"))
        max_players = int(request.form.get("max_players"))
        duration = int(request.form.get("duration"))

        new_game = {
            "game_title": request.form.get("game_title").lower(),
            "designer": request.form.get("designer").lower(),
            "min_players": min_players,
            "max_players": max_players,
            "avg_playtime_mins": duration,
            "difficulty": request.form.get("difficulty").lower(),
            "description": request.form.get("description"),
            "image": request.form.get("image"),
        }
        print(new_game)
        mongo.db.games.insert_one(new_game)

        flash("Game added successfully!")
        return redirect(url_for("library"))

    return render_template("add_game.html")


@app.route("/collection/<game_id>", methods=["GET", "POST"])
def collection(game_id):
    """_summary_ Allows user to add a game to their personal collection.
    Identifies the game and user.
    Flash message if game already exists in user collection.
    Add game id str to user collection arr.

    Args:
        game_id (_str_): Game ObjectId

    Returns:
        _page_: refreshed render page. DB updates, if conditions met.
    """
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    existing_collection = mongo.db.collections.find_one(
            {"username": user["username"]})

    if request.method == "POST":
        if str(game["_id"]) in existing_collection["user_collection"]:
            flash("You already have this game in your collection.")
        else:
            # Adds game Id string to user_collection arr
            mongo.db.collections.update_one(
                existing_collection,
                {"$push": {"user_collection": str(game["_id"])}})

    return redirect(url_for("library"))


@app.route("/delete_review/<review>/<game_id>", methods=["POST"])
def delete_review(review, game_id):
    """_summary_  Allows user to delete their own game reviews

    Args:
        review (_str_): Target review ObjectId
        game_id (_str_): game_id to pass to redirected game page

    Returns:
        _data_: displays full game info and all it's user reviews
        (Minus the review just deleted - as it no longer exists!)
    """
    # Finds & deletes the target review selected by the user
    mongo.db.reviews.delete_one({"_id": ObjectId(review)})

    return redirect(url_for('game', game_id=game_id))


@app.route("/logout")
def logout():
    # remove user from the session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
