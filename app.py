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
db = SQL("sqlite:///finance.db")


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
    stocks = db.execute("SELECT stock_id, stock_q FROM stonks WHERE user_id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id=?",session["user_id"])[0]["cash"]

    stock_info = [{
        "name": stock["stock_id"],
        "symbol": stock["stock_id"],
        "shares": stock["stock_q"],
        "price": round(lookup(stock["stock_id"])["price"], 2),
        "total": round(stock["stock_q"] * lookup(stock["stock_id"])["price"], 2)}
            for stock in stocks]

    gtotal = cash + sum(item['total'] for item in stock_info)

    return render_template("index.html", stock_info=stock_info, cash=cash, gtotal=gtotal)



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
        stock_index = request.form.get("symbol")
        quantity = int(request.form.get("shares"))
        cash = db.execute("SELECT cash FROM users WHERE id=?",session["user_id"])[0]["cash"]
        quoted = lookup(stock_index)
        if quoted is None:
            return apology("invalid symbol",400)
        price = quoted["price"]
        show = usd(price)
        name = quoted["name"]
        symb = quoted["symbol"]
        total = price*quantity
        if total > cash:
            return apology("You have not enough money to complete ", 400)
        after = round(cash - total, 2)
        now = datetime.datetime.now(pytz.timezone("US/Eastern"))

        #check if user already has stock that needs to be updated or we need to insert new .
        check = db.execute("SELECT * FROM stonks WHERE user_id=? AND stock_id=?",session["user_id"],symb)
        if len(check) == 0:
            db.execute("INSERT INTO stonks (user_id, stock_id, stock_q) VALUES (?,?,?)", session["user_id"],symb,quantity)
        if len(check) != 0:
             old = db.execute("SELECT stock_q FROM stonks WHERE user_id = ? AND stock_id = ?", session["user_id"], symb)
             new =  int(old[0]["stock_q"] + quantity)
             db.execute("UPDATE stonks SET stock_q = ? WHERE user_id=? AND stock_id = ?",new, session["user_id"],symb)


        db.execute("INSERT INTO transactions (user_id,stock_id,stock_price,stock_value,type,time,shares) VALUES(?,?,?,?,'buy',?,?)", session["user_id"],name ,price, total,now,quantity)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", after, session["user_id"])

        return redirect("/")

@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT * FROM transactions ")

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
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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

        q = request.form.get("symbol")
        quoted = lookup(q)
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
        db.execute("INSERT INTO users(username,hash,cash) VALUES (?,?,10000)", name, hashed_password)

        return redirect("/")








    #if GET etc redirecting to reg  page from menu
    if request.method =="GET":
        return render_template("register.html")

    """Register user"""



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        stocks = db.execute("SELECT stock_id FROM stonks WHERE user_id=?", session["user_id"])
        return render_template("sell.html", stocks=stocks)


    if request.method == "POST":
        if not request.form.get("symbol"):
         return apology("must provide stock symbols", 400)
        if not request.form.get("shares"):
            return apology("must provide amount to be purchased", 400)
        data = db.execute("SELECT stock_id,stock_q FROM stonks WHERE user_id=?", session["user_id"])

        symbol = request.form.get("symbol")
        quantity = int(request.form.get("shares"))

        quote = lookup(symbol)["price"]

        cash = db.execute("SELECT cash FROM users WHERE id=?",session["user_id"])[0]["cash"]
        shares = db.execute("SELECT stock_q FROM stonks WHERE user_id=? AND stock_id=?",session["user_id"],symbol)[0]["stock_q"]

        new_cash = quote*shares + cash
        db.execute("UPDATE users SET cash = ? WHERE id =?",new_cash, session["user_id"])
        new_shares = shares-quantity
        now = datetime.datetime.now(pytz.timezone("US/Eastern"))
        if new_shares > 0:
            db.execute("UPDATE stonks SET stock_q = ? WHERE user_id = ? AND stock_id = ?",new_shares ,session["user_id"] ,symbol )
            db.execute("INSERT INTO transactions (user_id,stock_id,stock_price,stock_value,type,time,shares) VALUES(?,?,?,?,'sell',?,?)", session["user_id"],symbol ,quote,quote*shares,now,shares)
        if new_shares == 0:
            db.execute("UPDATE stonks SET stock_q = 0 WHERE user_id = ? AND stock_id = ?", session["user_id"],symbol)
            db.execute("INSERT INTO transactions (user_id,stock_id,stock_price,stock_value,type,time) VALUES(?,?,?,?,'sell',?,?)", session["user_id"],symbol ,quote,quote*shares,now,quantity)
            db.execute("DELETE FROM stonks WHERE stock_id = ? AND user_id = ?",symbol,session["user_id"])
        if new_shares < 0:
            return apology("Not enough shares",400)


        return redirect("/")

















