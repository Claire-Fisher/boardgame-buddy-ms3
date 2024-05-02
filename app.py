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
    """Gets all the games from the db and sends to library template

    Returns:
        _template_ library.html
        _arr_: All games in db
    """

    games = list(mongo.db.games.find())
    return render_template("library.html", games=games)


@app.route("/search", methods=["GET", "POST"])
def search():
    """Checks user search inputs and filters the games db.

    Returns:
        _template_ library.html
        _arr_: _filtered game list_
    """

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

    new_search = request.form.get("search")
    if not new_search:
        pass
    else:
        query["$text"] = {"$search": new_search}
        games = list(mongo.db.games.find(query))

    if not query:
        flash("You didn't enter any search fields")
        return redirect('library')

    return render_template("library.html", games=games)


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registers a profile account.
    Calls new_collection().

    Returns:
        Success: _template_ library.html
        Fail: _template_ register.html
    """

    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        new_register = {
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
        mongo.db.users.insert_one(new_register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        # Generate empty collection obj for the user
        new_collection(session["user"])
        flash("Registration Successful!")
        return redirect(url_for("library"))

    return render_template("register.html")


@app.route("/new_collection/<username>", methods=["POST"])
def new_collection(username):
    """Creates an empty collection obj for the user
    Called from register()

    Args:
        username (_string_):

    Returns:
        _template_: library
    """

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
    """Checks the username and hashed password.
    User feedback if login successful/unsuccessful.

    Returns:
        _template_: library
    """

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
                flash(f"Welcome, {session["user"].capitalize()}")
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
    """Security checks for an active user and a match with username.
    Fetches session users info and collection
    and renders their profile page.

    Args:
        username (_str_)

    Returns:
        _template_: profile
    """
    if not session.get("user") or session["user"] != username:
        return redirect(url_for('library'))
    else:
        info = mongo.db.users.find_one({"username": username})

        # Turns user avatar into a string
        avatar = info.get("avatar_url")
        avatar = str(avatar)

        # Fetches collection by user id
        collection_obj = mongo.db.collections.find_one(
            {"user_id": str(info["_id"])})
        collection = collection_obj["user_collection"]

        # Creates an arr of tuples (image, title, game_id)
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
    """Delete functionality.
    Gets the user collection games.
    User can remove games from their collection.

    Args:
        game_id (_str_): Game ObjectId

    Returns:
        profile()
        Refreshes profile page with deleted game instantly removed.
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
    """Update functionality. Fetches user profile info and populates form
    Placeholders if data field is empty. Profile data updated on submit.

    Args:
        username (_str_)
        placeholder (_str_, optional) Defaults to None.

    Returns:
        _template_: profile (with updated data)
    """

    if not session.get("user") or session["user"] != username:
        return redirect(url_for('library'))
    else:
        info = mongo.db.users.find_one({"username": username})
        # placeholder instructions for user if values are blank
        placeholder = {
            "city":
                "Enter your City here" if info["city"] == "" else "",
            "country":
                "Enter your Country here" if info["country"] == "" else "",
            "favourite_game":
                "Enter your favourite game here"
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
            flash("Profile Successfully Updated")
            return redirect(url_for("profile", username=username))

        return render_template(
            "edit_profile.html",
            info=info,
            placeholder=placeholder,
            avatar=avatar)


@app.route("/game/<game_id>", methods=["GET", "POST"])
def game(game_id):
    """Fetches full info, inc reviews, for the game selected by the user.
    Add review functionality if active session user.

    Args:
        game_id (_str_): Game ObjectId

    Returns:
        _template_: game.html
        Displays full game info and all it's user reviews
    """

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    relevant_reviews = list(mongo.db.reviews.find({"game_id": game_id}))

    # Check if a user is logged in for write review functionality
    username = None
    if "user" in session:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        if request.method == "POST":
            new_review = {
                "game_id": game_id,
                "game_title": game["game_title"],
                "review": request.form.get("review"),
                "review_title": request.form.get("review-title"),
                "username": username,
            }
            mongo.db.reviews.insert_one(new_review)
            # Adds the new review to the end of the relevant reviews list
            relevant_reviews.append(new_review)

    return render_template(
        "game.html", game=game, relevant_reviews=relevant_reviews)


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    """Create functionality, add games to the library.

    Returns:
        library() OR add_game()
    """
    if not session.get("user"):
        return redirect(url_for('library'))
    else:
        if request.method == "POST":
            existing_game = mongo.db.games.find_one(
                {"game_title": request.form.get("game_title").lower()})

            if existing_game:
                flash("That game already exists")
                return redirect(url_for("add_game"))

            # Converts str data from form into integers & stores in variables
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

            mongo.db.games.insert_one(new_game)
            flash("Game added successfully!")
            return redirect(url_for("library"))

        return render_template("add_game.html")


@app.route("/collection/<game_id>", methods=["GET", "POST"])
def collection(game_id):
    """Edit functionality, add a game to user's personal collection.
    Flash message if game already exists in user collection.
    Add game id str to user collection arr.

    Args:
        game_id (_str_): Game ObjectId

    Returns:
        library().
        DB updates, if conditions met.
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
            flash("Game successfully added to your collection")

    return redirect(url_for("library"))


@app.route("/delete_review/<review>/<game_id>", methods=["POST"])
def delete_review(review, game_id):
    """Delete functionality, user deletes their own game reviews

    Args:
        review (_str_): Target review ObjectId
        game_id (_str_): game_id to pass to redirected game page

    Returns:
        game().
        Refreshes full game info and all it's user reviews
        (Minus the review just deleted - as it no longer exists!)
    """

    mongo.db.reviews.delete_one({"_id": ObjectId(review)})

    return redirect(url_for('game', game_id=game_id))


@app.route("/edit_review/<review>/<game_id>", methods=["POST"])
def edit_review(review, game_id):
    """Edit functionality, user edits their own game reviews

    Args:
        review (_str_): Target review ObjectId
        game_id (_str_): game_id to pass to redirected game page

    Returns:
        game().
        Refreshes full game info and all it's user reviews
    """

    if not session.get("user"):
        return redirect(url_for('library'))
    else:

        if request.method == "POST":
            save_review = {
                "review_title": request.form.get("edit_review_title").lower(),
                "review": request.form.get("edit_review")
            }

            mongo.db.reviews.update_one(
                {"_id": ObjectId(review)}, {"$set": save_review})
            flash("Review Successfully Updated")
            game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
            relevant_reviews = list(
                mongo.db.reviews.find({"game_id": game_id}))
            # After updating the review, render the game template directly
            return render_template(
                "game.html", game=game, relevant_reviews=relevant_reviews)

        # If the request is not POST, redirect to the game route
        return redirect(url_for("game", game_id=game_id))


@app.route("/logout")
def logout():
    """Logs out the user. Removes user from the session cookie

    Returns:
        login()
    """

    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    """
    404 Error handler
    """
    try:
        return render_template('404.html'), 404
    except Exception as e:
        return "Ann error occurred", 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
