import sqlite3
import os
from flask import Flask, request, redirect, url_for, render_template, g, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

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
        password = request.form["password"]
        dob = request.form["dob"]
        print(username,email,password)
        db = get_db()
        existing_user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        #calculation for the date to make sure the user is over 18
        dob = datetime.strptime(dob,'%Y-%m-%d').date()
        today = date.today()

        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        #conditions for registering
        if age < 18:
            return render_template("register.html", error="Must be at least 18 years old to register")
        
        if existing_user:
            return render_template("register.html", error="This email is already in use")

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
        "SELECT * FROM cocktails ORDER BY popularity/reviews_number DESC LIMIT 5"
    ).fetchall()

    return render_template('homepage.html', top_cocktails=top_cocktails)

@app.route('/homepage.html')
def homepage():
    db = get_db()
    top_cocktails = db.execute(
        "SELECT * FROM cocktails ORDER BY popularity/reviews_number DESC LIMIT 5"
    ).fetchall()

    return render_template('homepage.html', top_cocktails=top_cocktails)

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

@app.route('/pantry.html', methods=['GET'])
def pantry():
    db = get_db()
    ingredients = db.execute("SELECT * FROM ingredients").fetchall()
    return render_template("pantry.html", ingredients=ingredients)

@app.route('/get_cocktails', methods=['POST'])
def get_cocktails():
    selected_ingredients = request.json.get("ingredients", [])
    
    if not selected_ingredients:
        return jsonify([])  # No ingredients selected

    db = get_db()
    placeholders = ",".join("?" * len(selected_ingredients))

    query = f"""
        SELECT c.id, c.name 
        FROM cocktails c
        JOIN cocktail_ingredients ci ON c.id = ci.cocktail_id
        WHERE ci.ingredient_id IN ({placeholders})
        GROUP BY c.id
        HAVING COUNT(DISTINCT ci.ingredient_id) >= ?
    """

    print("Selected Ingredients:", selected_ingredients)  # Debugging print

    cocktails = db.execute(query, selected_ingredients + [len(selected_ingredients)]).fetchall()

    return jsonify([{"id": c["id"], "name": c["name"]} for c in cocktails])

@app.route('/creation.html', methods=['GET', 'POST'])
def creation():
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']
        alcohol_content = int(request.form['alcohol_content'])
        method = request.form['method']
        recipe_by = session.get('username', 'Anonymous')

        selected_ingredients = request.form.get('selected_ingredients', '')

        db.execute(
            "INSERT INTO cocktails (name, image, popularity, reviews_number, alcohol_content, recipe_by, ingredients) VALUES (?, '', 5, 1, ?, ?, ?)",
            (name, alcohol_content, recipe_by, selected_ingredients)
        )
        db.commit()
        flash("Cocktail added successfully!", "success")
        return redirect(url_for('explore'))

    ingredients = db.execute("SELECT * FROM ingredients").fetchall()
    return render_template('creation.html', ingredients=ingredients)

@app.route('/userpage.html')
def user_profile():

     if "user_id" not in session:
         flash("You need to log in to view your profile!", "danger")
         return redirect(url_for("login"))
     
     db = get_db()
     user_id = session["user_id"]

     user_info = db.execute("SELECT *  FROM users WHERE id = ?", (user_id,)).fetchone()

     # Fetch cocktails created by the logged in user 
     user_cocktails = db.execute(
        "SELECT * FROM cocktails WHERE user_id = ?", (user_id,)
     ).fetchall()

     if user_info is None:
        flash("User not found!", "danger")
        return redirect(url_for("login"))

     return render_template("userpage.html", user_cocktails=user_cocktails)


if __name__ == '__main__':
    app.run(debug = True)
