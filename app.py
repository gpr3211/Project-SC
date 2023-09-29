import os
import pytz
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///scorpio.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
  
    return render_template("index.html")



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    if request.method == "POST":
        if not request.form.get("symbol"):
         return apology("must provide stock symbols", 400)
        if not request.form.get("shares"):
            return apology("must provide amount to be purchased", 400)
       
        return redirect("/")

@app.route("/history")
@login_required
def history():
   
    return render_template("history.html", transactions=transactions)






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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash_pass"], request.form.get("password")):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")


    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must provide stock index eg. TSLA for Tesla", 400)

        if quote is None:
            return apology("invalid symbol",400)
        return render_template("quoted.html", quoted=quoted)





@app.route("/register", methods=["GET", "POST"])
def register():
    #since we are registering a new user, make sure we log out existing ones
    session.clear()
    #in case POST etc getting a submit form
    if request.method =="POST":
        row = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(row) !=0 :
            return apology("Username already taken", 400 )
        name = request.form.get("username")
        password = request.form.get("password")
        conf = request.form.get("confirmation")
        if not name or not password:
            return apology("Empty name or password field",400)
        if password != conf:
            return apology("Confirm doesnt match Password", 400)
        hashed_password = generate_password_hash(password)
        length = db.execute("SELECT COUNT(*) FROM users")
        db.execute("INSERT INTO users(username,hash_pass) VALUES (?,?)", name, hashed_password)

        return redirect("/")








    #if GET etc redirecting to reg  page from menu
    if request.method =="GET":
        return render_template("register.html")

    """Register user"""



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
   


        return redirect("/")

















