"""
To do:
Format date
Delete from History
History filters
"""
import os
import sqlite3
import time
from time import struct_time
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# set databae for app
conn = sqlite3.connect("minimeals.db", check_same_thread=False)
conn.row_factory  =sqlite3.Row
db = conn.cursor()

@app.route("/")
@login_required
def index():   
    # display child name and last entry
    db.execute("SELECT * FROM meals WHERE user_id=(?) ORDER BY date DESC", (session["user_id"], ))
    row = db.fetchone()
    if not row:
        flash("You were successfully logged in but have no meals to show", "primary")
        return render_template("index_initial.html", username = session["username"], child = session["child"])
    else:
        db.execute("""SELECT dishes.name from dishes INNER JOIN meals_to_dishes 
                    ON dishes.id=meals_to_dishes.dish_id WHERE meals_to_dishes.meal_id=(?)""", (row["id"], ))
        dishes = list(db.fetchall())
        flash('You were successfully logged in', 'success')
        return render_template("index.html", username = session["username"], child = session["child"], row = row, dishes = dishes)
    

@app.route("/record", methods=["GET", "POST"])
@login_required
def record():
    return render_template("record.html")

@app.route("/add_meal", methods=["GET", "POST"])
@login_required
def add_meal():
    # check date, meal and at least one dish entered
    if not request.form.get("date") or not request.form.get("meal") or not request.form.get("dish0"):
        flash("You must select a date, a meal and at least one dish", "danger")
        return render_template("record.html")
    # loop over and check each dish exists
    for i in range(5):
        dish = request.form.get("dish" + str(i)).casefold()
        if dish:
            db.execute("SELECT * from dishes WHERE name=(?)", (dish, ))
            row = db.fetchone()
            if not row:
                flash(str(dish) + "-this dish doesn't exist - please add below and try again", "danger")
                return render_template("record.html")
        else:
            pass
    # enter user_id, meal, amount, mood, date and notes into users table
    db.execute("INSERT INTO meals (user_id, meal, amount, mood, date, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (session["user_id"], request.form.get("meal"), request.form.get("amount"), 
                request.form.get("mood"), request.form.get("date"), request.form.get("notes")))
    conn.commit()
    # get meal_id, and lopp over dishes to put dish_id into meals_to_dishes
    meal_id = db.lastrowid
    for i in range(5):
        dish = request.form.get("dish" + str(i))
        if dish:
            db.execute("SELECT * from dishes WHERE name=(?)", (dish.casefold(), ))
            row = db.fetchone()
            dish_id = row["id"]
            db.execute("INSERT INTO meals_to_dishes (meal_id, dish_id) VALUES (?, ?)", (meal_id, dish_id))
            conn.commit()
        else:
            pass
    conn.commit()
    flash("Meal added successfully", "success")
    return render_template("record.html")

@app.route("/add_dish", methods=["GET", "POST"])
@login_required
def add_dish():
    # check a dish name and at least one ingredient was added
    if not request.form.get("dish") or not request.form.get("ingredient0"):
        flash("You mut suply a dish name and at least one ingredient", "danger")
        return render_template("record.html")
    # check dish is uniques
    db.execute("SELECT * FROM dishes WHERE name=(?)", (request.form.get("dish"), ))
    row = db.fetchone()
    if row:
        flash("Dish name already exists - please use this one or create a unique name", "danger")
        return render_template("record.html")
    # add dish to database and get id
    db.execute("INSERT INTO dishes (name) VALUES (?)", (request.form.get("dish").casefold(), ))
    conn.commit()
    # db.execute("SELECT * from dishes WHERE name=(?)", (request.form.get("dish"), ))
    # row = db.fetchone() I don't need these lnes any more!
    dish_id = db.lastrowid
    # add all ingredients and add them to databse
    for i in range(5):
        ingredient = request.form.get("ingredient" + str(i))
        if ingredient:
            db.execute("SELECT * from ingredients WHERE name=(?)", (ingredient.casefold(), ))
            row = db.fetchone
            if row:
                db.execute("INSERT INTO ingredients (name) VALUES (?)", (ingredient.casefold(), ))
                conn.commit()
            else:
                pass
            # db.execute("SELECT * from ingredients WHERE name=(?)", (ingredient, ))
            # row = db.fetchone()
            ingredient_id = db.lastrowid
            db.execute("INSERT INTO dishes_to_ingredients (dish_id, ingredient_id) VALUES (?, ?)", (dish_id, ingredient_id))
            conn.commit()
        else:
            pass
    conn.commit()
    flash("Dish added sucessfully", "success")
    return render_template("record.html")

@app.route("/review", methods=["GET", "POST"])
@login_required
def review():
    db.execute("SELECT * FROM meals WHERE user_id=(?) ORDER BY date DESC", (session["user_id"], ))
    rows = db.fetchall()
    if not rows:
        flash("You don't have any meals to review yet, why not log some?", "primary")
        return render_template("index_initial.html", username = session["username"], child = session["child"])
    else:
        dishlist = []
        for row in rows:
            db.execute("""SELECT dishes.name from dishes INNER JOIN meals_to_dishes 
                    ON dishes.id=meals_to_dishes.dish_id WHERE meals_to_dishes.meal_id=(?)""", (row["id"], ))
            dishes = list(db.fetchall())
            dishlist.append(dishes)
        results = zip(rows, dishlist)
    return render_template("review.html", username = session["username"], child = session["child"], results = results)

"""
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        pass
    else:
        return render_template("contact.html")
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("You must provide a username", "danger")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please provde a password", "danger")
            return render_template("login.html")
        # Query database for username
        db.execute("SELECT * FROM users WHERE username = :username", dict(username=request.form.get("username")))
        rows = db.fetchone()

        # Ensure username exists and password is correct
        if rows == None or not check_password_hash(rows[2], request.form.get("password")):
            flash("Invalid username and/or password", "danger")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows["id"]
        session["username"] = rows["username"]
        session["child"] = rows["child"]

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


@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    if request.method == "POST":
        # apology if username blank
        if not request.form.get("username"):
            return apology("You must provide a username")
        # apology if username already exists
        db.execute("SELECT * FROM users WHERE username=(?)", (username, ))
        rows = db.fetchone()
        if rows != None:
            return apology("Username must be unique")
        # apology if password or confirmation blank or both don't match
        if not request.form.get("password") or not request.form.get("confirmation") or not request.form.get("child") or request.form.get("password") != request.form.get("confirmation"):
            return apology("Please enter matching passwords and a child's name")
        # insert new user into users, storing hash of pasword
        db.execute("INSERT INTO users (username, hash, child) VALUES (:username, :hash, :child)",
                    dict(username = request.form.get("username"),
                    hash =  generate_password_hash(request.form.get("password")),
                    child = request.form.get("child")))
        conn.commit()
        # login
        db.execute("SELECT * FROM users WHERE username =(?)", (username,))
        rows = db.fetchone()
        session["user_id"] = rows[0]
        session["username"] = rows[1]
        session["child"] = rows[3]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        # check if any field blank
        if not request.form.get("password") or not request.form.get("newpass") or not request.form.get("newpass2"):
            flash("You must fill in all fields", "danger")
            return render_template("account.html")
        # check that password changes match
        if request.form.get("newpass") != request.form.get("newpass2"):
            flash("New password doesn't match", "danger")
            return render_template("account.html")
        #check correct password entered
        db.execute("SELECT * FROM users WHERE id = :user_id", dict(user_id = session["user_id"]))
        row = db.fetchone()
        # Check password is correct
        if not check_password_hash(row["hash"], request.form.get("password")):
            flash("invalid username and/or password", "danger")
            return render_template("account.html")
        # update password
        db.execute("UPDATE users SET hash = :hash WHERE id = :user_id",
            dict(hash = generate_password_hash(request.form.get("newpass")), user_id = session["user_id"]))
        conn.commit()
        flash("Password changed successfully", "success")
        return render_template("account.html")
    else:
        return render_template("account.html", child = session["child"])

@app.route("/change_child", methods=["GET", "POST"])
@login_required
def change_child():
    if request.method == "POST":
        # check if any field blank
        if not request.form.get("newchild") or not request.form.get("newchild2"):
            flash("You must fill in all fields", "danger")
            return render_template("account.html", child = session["child"])
        # check that password changes match
        if request.form.get("newchild") != request.form.get("newchild2"):
            flash("New child's name doesn't match", "danger")
            return render_template("account.html", child = session["child"])
        # update password
        db.execute("UPDATE users SET child=(?) WHERE id =(?)", (request.form.get("newchild"), session["user_id"]))
        conn.commit()
        session["child"] = request.form.get("newchild")
        flash("Child's name changed successfully", "success")
        return render_template("account.html", child = session["child"])
    else:
        return render_template("account.html", child = session["child"])


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
