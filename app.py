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

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        branches = db.execute("SELECT * FROM branches")
        equipments = db.execute("SELECT * FROM equipment")
        return render_template("quote.html", equipments=equipments,branches=branches )


    if request.method == "POST":
        if not request.form.get("primary"):
            return apology("Must provide primary muscle group eg. arms or back", 400)
        if not request.form.get("equipment"):
            return apology("Must check at least 1 equipment",420)
        if quote is None:
            return  apology("must provide inputs",420)
        
        
        primary = request.form.get("primary")
        secondary = request.form.get("secondary")
        equipment = request.form.get("equipment")
        len_eq = len(equipment)
        
        comments = db.execute("SELECT * from comments WHERE ex_id IN (SELECT ex_id FROM exercises WHERE (ex_branch = ? OR ex_branch = ?) AND (ex_equip = ?)) ",primary,secondary,equipment[0])
        
        
       ## exercises = db.execute("SELECT * FROM exercises WHERE (ex_branch = ? OR ex_branch = ?) AND (ex_equip = ?)",primary,secondary,equipment[0])
        exercises = db.execute("SELECT * FROM exercises WHERE (ex_branch = ? OR ex_branch = ?) AND (ex_equip = ?)",primary,secondary,equipment[0])
        #one = exercises[0]["ex_id"]
        #    two = exercises[1]["ex_id"]
        #    three = exercises[2]["ex_id"]
        #    four = exercises[3]["ex_id"]
        #    five = exercises[4]["ex_id"]
            
        #db.execute("INSERT INTO workouts (w_one,w_two,w_three,w_four,w_five,int_id) values (?,?,?,?,?,1)",one,two,three,four,five)

        
        return render_template("quoted.html", exercises = exercises, comments=comments)







@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    

    
    if request.method == "GET":
        
        if session["user_id"] == 1:
            branches = db.execute("SELECT * FROM branches")
            equipments = db.execute("SELECT * FROM equipment")
            exercises = db.execute("SELECT * FROM exercises")
            return render_template("admin.html", equipments=equipments,branches=branches,exercises = exercises )
        else:
            return apology("You must be admin to access this page",420)


    if request.method == "POST":
       
        primary = request.form.get("primary")
        secondary = request.form.get("secondary")
        branch = request.form.get("branch")
        equip = request.form.get("equip")
        comment = request.form.get("comment")
        name = request.form.get("name")
        image = request.form.get("image")
        remove = request.form.get("remove")
        
        #add coment to exercise
        db.execute("UPDATE exercises SET comment =  ? WHERE ex_id = ?",secondary,primary)
        branches = db.execute("SELECT * FROM branches")
        equipments = db.execute("SELECT * FROM equipment")
        exercises = db.execute("SELECT * FROM exercises")
        if name:

            db.execute("INSERT INTO exercises (ex_name,ex_branch,ex_equip,ex_img,comment) VALUES (?,?,?,?,?)",name,branch,equip,image,comment)
    

    
        if remove:

            db.execute ("DELETE FROM exercises where ex_id = ?",remove)



        
        
        
        return render_template("admin.html",equipments=equipments,branches=branches,exercises = exercises )







@app.route("/history")
@login_required
def history():
   
    return render_template("history.html", )






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

















