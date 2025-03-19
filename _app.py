import ast
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, json
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from search import search_car_parts

from fill_db import fill_db
import excel_reader

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# flags to avoid two big updates at the same time -- Prototype --
db_system_state = SQL("sqlite:///state.db")
db_system_state.execute("UPDATE system SET state = (?) WHERE name = (?)", "chill", "big_update")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/result", methods=["GET", "POST"])
@login_required
def result():
    user = session["user_id"]
    try:
        input_search = request.args.get("search")
        print(input_search)
        input_list = re.split(",| ", input_search)
        
        for input in input_list:
            if input == " " or input == "":
                input_list.remove(input)

        parts_info = search_car_parts(input_list, user, "database.db")

        return render_template("result.html", parts=parts_info, favorites=favorites())

    except Exception as e:
        return render_template("result.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # logged user id
    user = session["user_id"]

    """Show most viewed or favorites parts"""
    # if request.method == "GET":

    # favorites
    favorites = db.execute("""SELECT car_parts.name, car_parts.reference
                            FROM car_parts WHERE car_parts.id IN
                            (SELECT part_id FROM favorites_by_users WHERE user_id = ?)""", user)
    
    return render_template("index.html", parts=favorites)


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    """Show favorites parts"""
    # logged user id
    user = session["user_id"]

    # favorites
    favorites = db.execute("""SELECT car_parts.name, car_parts.reference
                            FROM car_parts WHERE car_parts.id IN
                            (SELECT part_id FROM favorites_by_users WHERE user_id = ?)""", user)

    # render the page and pass the history info
    return render_template("favorites.html", favorites=favorites)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add new part reference."""
    # Submit the new part to the database parts.db
    if request.method == "POST":
        # get info for the new part from the form
        name = request.form.get("name")
        reference = request.form.get("reference")
        car_brand_name = request.form.get("car_brand")
        part_manufacturer_name = request.form.get("part_manufacturer")
        input_tags = request.form.get("tags")

        # transform into a python list
        if not input_tags:
            input_tags = "sem tags"
        tags_list = input_tags.split(",")
        tags_list = [tag.strip() for tag in tags_list]

        # check if the reference already exist
        reference_check = db.execute("SELECT id FROM car_parts WHERE reference LIKE ?", reference)
        if reference_check:
            return apology("Reference already exists")

        # id for the car brand
        car_brand = db.execute("SELECT id FROM car_brands WHERE name LIKE ?", car_brand_name)
        if not car_brand:
            car_brand_id = db.execute(
                "INSERT INTO car_brands (name) VALUES (?)", str(car_brand_name))
            # return apology("car brand not valid")
        else:
            car_brand_id = car_brand[0]['id']

        # if for the manufacturer
        part_manufacturer = db.execute(
            "SELECT id FROM part_manufacturers WHERE name LIKE ?", part_manufacturer_name)
        if not part_manufacturer:
            part_manufacturer_id = db.execute(
                "INSERT INTO part_manufacturers (name) VALUES (?)", str(part_manufacturer_name))
            # return apology("part manufacturer not valid")
        else:
            part_manufacturer_id = part_manufacturer[0]["id"]

        # create the new part without the tags
        new_part_id = db.execute("INSERT INTO car_parts (name, reference, car_brand_id, part_manufacturer_id) VALUES(?, ?, ?, ?)",
                                 name.capitalize(), reference.upper(), int(car_brand_id), int(part_manufacturer_id))

        # insert the tags into the part - tag table, many-to-many relation
        for tag_name in tags_list:
            # if the tag is already in the tag table get the id
            tag = db.execute(" SELECT id FROM tags WHERE name LIKE ? ", tag_name)

            # if the tag is not in the table inserts
            if not tag:
                tag_id = db.execute("INSERT INTO tags (name) VALUES (?)", tag_name)
            else:
                tag_id = tag[0]["id"]

            # inserts the pair in the table
            db.execute("INSERT INTO car_parts_tags (tag_id, part_id) VALUES (?, ?)",
                       tag_id, new_part_id)

        return render_template("added.html", name=name, reference=reference, car_brand=car_brand_name, part_manufacturer=part_manufacturer_name)

    else:
        # """Get the current state for the big_update"""
        # big_update_state = db_system_state.execute("SELECT state FROM system WHERE name = (?)", "big_update")[0]["state"]
        # print(big_update_state)

        # if big_update_state == "chill":
        #     flash('Updating database. You can reload the page and keep navigating.')
        #     db_system_state.execute("UPDATE system SET state = (?) WHERE name = (?)", "updating", "big_update")

        #     """Get data from excel file"""
        #     data = excel_reader.get_parts_data('referencias.xlsx')

        #     """insert the data on the database"""
        #     if data:
        #         fill_response = fill_db(db, data)
        #         print(fill_response)
        #         db_system_state.execute("UPDATE system SET state = (?) WHERE name = (?)", "chill", "big_update")
        #     else:
        #         print("No data file found")
        #         db_system_state.execute("UPDATE system SET state = (?) WHERE name = (?)", "chill", "big_update")
        # else:
        #     print("Update in course")

        # Get input from user for new car part
        return render_template("add.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Check for username blank
        if not request.form.get("username"):
            return apology("must provide a username")

        # Check for duplicate
        users = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if users:
            return apology("username already in use")

        # Check for password blank
        if not request.form.get("password"):
            return apology("must provide a password")

        #  Check for blank confirmation and if equal password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation must not be blank and must match")

        # Register
        password_hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   request.form.get("username"), password_hash)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """Edit car part information"""
    if request.method == "POST":
        print("request.form: ", request.form)

        part_info = request.form.get("part_info")
        part_info = ast.literal_eval(part_info)

        input_tags = request.form.get("tags")


        # transform into a python list
        tags_list = input_tags.split(",")
        tags_list = [tag.strip() for tag in tags_list]

        for tag in tags_list:
            if not tag == "":
                # if the tag is already in the tag table get the id
                tag_id = db.execute(" SELECT id FROM tags WHERE name LIKE ? ", tag)

                # if the tag is not in the table inserts and get tag id
                if not tag_id:
                    tag_id = db.execute("INSERT INTO tags (name) VALUES (?)", str(tag))
                else:
                    tag_id = tag_id[0]["id"]

                print("tag id:", tag_id)
                car_pats_tags_pair = db.execute(
                    "SELECT * FROM car_parts_tags WHERE part_id = ? AND tag_id = ?", part_info["id"], tag_id)

                # check if the part tag pair exists
                if not car_pats_tags_pair:
                    # inserts the pair in the table
                    db.execute("INSERT INTO car_parts_tags (tag_id, part_id) VALUES (?, ?)",
                            tag_id, part_info["id"])

        print(tags_list)
        return render_template("updated.html", reference=part_info["reference"], tags_list=tags_list)

    else:
        reference = request.args.get("reference")

        part_info = db.execute("SELECT * FROM car_parts WHERE reference LIKE ?", reference)

        if part_info:
            part_info = part_info[0]
            tags_info = db.execute("""SELECT * FROM tags WHERE id IN
                                    (SELECT tag_id FROM car_parts_tags
                                    WHERE part_id = ?)""", part_info["id"])

        return render_template("update.html", part_info=part_info, tags_info=tags_info)


@app.route("/favorite")
@login_required
def favorite():
    """Add new favorite"""
    # logged user id
    user = session["user_id"]

    part_reference = request.args.get("reference")

    part_id = db.execute("SELECT id FROM car_parts WHERE reference = ?", part_reference)[0]["id"]

    exist = db.execute(
        "SELECT * FROM favorites_by_users WHERE part_id = ? and user_id = ?", part_id, user)

    if exist:
        db.execute("DELETE FROM favorites_by_users WHERE part_id = ? and user_id = ?", part_id, user)
        return jsonify(message="removed")
    else:
        db.execute("INSERT INTO favorites_by_users (part_id, user_id) VALUES (?, ?)", part_id, user)
        return jsonify(message="added")


@app.route("/remove_tag", methods=["GET", "POST"])
@login_required
def remove_tag():
    # logged user id
    user = session["user_id"]

    if request.method == "POST":
        info = request.get_json()


        if user == user:  # later will be implement-> just some users are authorized to delete part tags
            db.execute("DELETE FROM car_parts_tags WHERE tag_id = ? AND part_id = ?", info["tag_id"], info["part_id"])
            tag_id = db.execute("SELECT * FROM car_parts_tags WHERE tag_id = (?)", info["tag_id"])

            # if theres no other pair part tag delete the tag from tags
            if not tag_id:
                db.execute("""DELETE FROM tags WHERE id = (?)""", info["tag_id"])

            return jsonify(message="deleted", info=info)
        else:
            return jsonify(message="unauthorized user", info=info)
