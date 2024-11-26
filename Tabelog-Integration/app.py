from sqlite3 import connect, Cursor
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Initialize SQL DB
con = connect("birthdays.db", check_same_thread=False)
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

        name = request.form['name']
        month = int(request.form['month'])
        day = int(request.form['day'])
        print(f"name: {name}, month: {month}, day: {day}")
        print((name, month, day))
        cur.execute("INSERT INTO birthdays (name, month, day) VALUES (:name, :month, :day)", name=name, month=month, day=day)
        return redirect("/")

    else:

        rows = cur.execute("SELECT * FROM birthdays")
        return render_template("index.html", rows=rows)


@app.route("/remove", methods=["POST"])
def remove():
    id=request.form.get("id")
    cur.execute("DELETE FROM birthdays WHERE id = :id", id=id)
    return redirect("/")
