from sqlite3 import connect
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from bs4 import BeautifulSoup
import requests
import bcrypt

# Configure application
app = Flask(__name__)

#Configuring session type to auto logout everytime the site is closed
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Initialize SQL DB
con = connect("tabelog.db", check_same_thread=False)
cursor = con.cursor()

# Custom login_required decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        # Check if the user is logged in by looking for a session variable
        if 'user_id' not in session:
            return render_template("login.html")
        return f(*args, **kwargs)
    return wrapper

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":

        #extract url
        url = request.form.get('url')
            
        #check if url was provided
        if url:
            #check if submitted url was valid
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                #scrape website for name and address of restaurant
                name = soup.find('h2', class_='display-name').find('span').get_text(strip=True)
                address = soup.find('p', class_='rstinfo-table__address').get_text(strip=True)
                print((name, address))

    else:

        rows = cursor.execute("SELECT * FROM LOCATIONS")
        return render_template("index.html", rows=rows)


@app.route("/remove", methods=["POST"])
def remove():
    id=request.form.get("id")
    cursor.execute("DELETE FROM tabelog.db WHERE id = :id", id=id)
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        print(request.form.to_dict())

        if not request.form.get("username"):
            error_message = "Username not found"
            return render_template('login.html', error_message=error_message)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error_message = "Password not found"
            return render_template('login.html', error_message=error_message)
        
        rows = cursor.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists
        if len(rows) != 1:
            error_message = "Username does not exist"
            return render_template('login.html', error_message=error_message)
        
        # Ensure password is correct
        elif bcrypt.checkpw(password, rows[1]) == False:
            error_message = "Password incorrect"
            return render_template('login.html', error_message=error_message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            error_message = "Username not found"
            return render_template('register.html', error_message=error_message)

        # Ensure password(s) were submitted
        elif not request.form.get("password"):
            error_message = "Password not found"
            return render_template('register.html', error_message=error_message)

        elif not request.form.get("confirmation"):
            error_message = "Must confirm password"
            return render_template('register.html', error_message=error_message)

        # ensure passwords are identical
        if request.form.get("password") != request.form.get("confirmation"):
            error_message = "Confirmation unsuccessful"
            return render_template('register.html', error_message=error_message)

        rows = cursor.execute(
            "SELECT username FROM users WHERE username = ?", request.form.get("username")
        )

        # Verify if username already exists
        if len(rows) != 0:
            error_message = "Username already exists"
            return render_template('register.html', error_message=error_message)
        
        #generate password and hash
        password = request.form.get("password").encode('utf-8') # Convert password to bytes for compatibility with bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        # insert information
        rows = cursor.execute(
            "INSERT INTO users (username, hash) VALUES (?,?)", request.form.get(
                "username"), hashed_password
        )

        return redirect("/")

    else:
        return render_template("register.html")