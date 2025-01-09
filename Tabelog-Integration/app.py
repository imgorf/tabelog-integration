from sqlite3 import connect, Cursor
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from bs4 import BeautifulSoup
import requests

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
cur = con.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
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

        rows = cur.execute("SELECT * FROM LOCATIONS")
        return render_template("index.html", rows=rows)


@app.route("/remove", methods=["POST"])
def remove():
    id=request.form.get("id")
    cur.execute("DELETE FROM tabelog.db WHERE id = :id", id=id)
    return redirect("/")
