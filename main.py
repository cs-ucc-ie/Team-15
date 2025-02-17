import sqlite3
import os
from flask import Flask, request, redirect, url_for, render_template, g, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "my_secret_key" #for sessions

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "db.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()



@app.route('/register.html', methods=['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]  # Store plain text (NOT RECOMMENDED)
        print(username,email,password)
        db = get_db()
        existing_user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        db.commit()

        flash("Registration successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route('/login.html', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("homepage"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route('/')
def index():
    db = get_db()
    top_cocktails = db.execute(
        "SELECT * FROM cocktails ORDER BY popularity/reviews_number DESC LIMIT 4"
    ).fetchall()

    return render_template('homepage1.html', top_cocktails=top_cocktails)

@app.route('/homepage.html')
def homepage():
    db = get_db()
    top_cocktails = db.execute(
        "SELECT * FROM cocktails ORDER BY popularity/reviews_number DESC LIMIT 4"
    ).fetchall()

    return render_template('homepage1.html', top_cocktails=top_cocktails)

@app.route('/explore.html')
def explore():
    db = get_db()
    filter_option = request.args.get("filter", "all")
    
    query = "SELECT * FROM cocktails"
    params = []

    if filter_option == "alcoholic":
        query += " WHERE alcohol_content > 0"
    elif filter_option == "non-alcoholic":
        query += " WHERE alcohol_content = 0"
    elif filter_option == "easy":
        query += " ORDER BY popularity/reviews_number ASC"
    elif filter_option == "advanced":
        query += " ORDER BY popularity/reviews_number DESC"
    
    cocktails = db.execute(query, params).fetchall()

    return render_template("explore.html", cocktails=cocktails, filter_option=filter_option)

@app.route('/pantry.html')
def pantry():
    return render_template('pantry.html')

@app.route('/creation.html')
def creation():
    return render_template('creation.html')

# user profile page [My profile]
# @app.route('/userpage.html')
# def user_profile():
#     db = get_db()
#     user_id = session["user_id"]

#     if "user_id" not in session:
#         flash("You need to log in to view your profile!", "danger")
#         return redirect(url_for("login"))

#     # Fetch cocktails created by the logged in user 
#     user_cocktails = db.execute(
#         "SELECT * FROM cocktails WHERE user_id = ?", (user_id,)
#     ).fetchall()

#     return render_template("userpage.html", user_cocktails=user_cocktails)


if __name__ == '__main__':
    app.run(debug = True)
