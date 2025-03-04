import sqlite3
import os
from flask import Flask, request, redirect, url_for, render_template, g, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "my_secret_key" #for sessions

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "db.db")

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/register.html', methods=['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        dob = request.form["dob"]
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
    cocktail_id = request.args.get("id") #Debug
    
    print(cocktail_id)

    if cocktail_id:
        selected_cocktail = db.execute(
            "SELECT * FROM cocktails WHERE id = ?", (cocktail_id,)
        ).fetchone()

        ingredients = db.execute(
            """SELECT ingredients.name 
               FROM ingredients 
               JOIN cocktail_ingredients ON ingredients.id = cocktail_ingredients.ingredient_id 
               WHERE cocktail_ingredients.cocktail_id = ?""", (cocktail_id,)
        ).fetchall()

        reviews = db.execute(
            """SELECT reviews.rating, reviews.review_text, users.username, reviews.created_at 
               FROM reviews 
               JOIN users ON reviews.user_id = users.id 
               WHERE reviews.cocktail_id = ?
               ORDER BY reviews.created_at DESC""", (cocktail_id,)
        ).fetchall()

        print(reviews) #Debug

        return render_template("explore.html", selected_cocktail=selected_cocktail, ingredients=ingredients, reviews=reviews)

    filter_option = request.args.get("filter", "all")

    query = "SELECT * FROM cocktails"
    
    if filter_option == "alcoholic":
        query += " WHERE alcohol_content > 0"
    elif filter_option == "non-alcoholic":
        query += " WHERE alcohol_content = 0"
    elif filter_option == "easy":
        query += " ORDER BY CAST(popularity AS FLOAT) / reviews_number ASC"
    elif filter_option == "advanced":
        query += " ORDER BY CAST(popularity AS FLOAT) / reviews_number DESC"

    cocktails = db.execute(query).fetchall()

    return render_template("explore.html", cocktails=cocktails, filter_option=filter_option)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    db = get_db()
    
    # Get data from form
    user_id = session.get("user_id")  # Ensure user is logged in
    cocktail_id = request.form.get("cocktail_id")
    rating = request.form.get("rating")
    review_text = request.form.get("review_text", "")

    if not user_id:
        flash("You must be logged in to submit a review.", "error")
        return redirect(request.referrer)

    # Insert into database
    db.execute(
        "INSERT INTO reviews (user_id, cocktail_id, rating, review_text) VALUES (?, ?, ?, ?)",
        (user_id, cocktail_id, rating, review_text)
    )
    db.commit()

    # Update cocktail's popularity & review count
    db.execute(
        "UPDATE cocktails SET popularity = popularity + ?, reviews_number = reviews_number + 1 WHERE id = ?",
        (int(rating), cocktail_id)
    )
    db.commit()

    flash("Review submitted successfully!", "success")
    return redirect(request.referrer)

@app.route('/pantry.html', methods=['GET'])
def pantry():
    db = get_db()
    ingredients = db.execute("SELECT * FROM ingredients").fetchall()
    return render_template("pantry.html", ingredients=ingredients)

@app.route('/get_cocktails', methods=['POST'])
def get_cocktails():
    selected_ingredients = request.json.get("ingredients", [])
    
    if not selected_ingredients:
        return jsonify([])  #No ingredients selected

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
        created_by = session["user_id"]


        #Handle Image Upload
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        else:
            filename = 'basic.jpg'  #Default if no image uploaded

        #Get selected ingredient IDs
        selected_ingredient_ids = request.form.get('selected_ingredients', '')
        selected_ingredient_ids = [int(i) for i in selected_ingredient_ids.split(',') if i.isdigit()]

        #Insert into cocktails table
        cursor = db.execute(
            "INSERT INTO cocktails (name, image, popularity, reviews_number, alcohol_content, recipe_by, method, created_by) VALUES (?, ?, 5, 1, ?, ?, ?, ?)",
            (name, filename, alcohol_content, recipe_by, method, created_by)
        )
        cocktail_id = cursor.lastrowid

        #Insert into cocktail_ingredients table
        for ingredient_id in selected_ingredient_ids:
            db.execute(
                "INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id) VALUES (?, ?)",
                (cocktail_id, ingredient_id)
            )

        db.commit()
        flash("Cocktail added successfully!", "success")
        return redirect(url_for('explore'))

    ingredients = db.execute("SELECT * FROM ingredients").fetchall()
    return render_template('creation.html', ingredients=ingredients)

@app.route('/userpage.html')
def userpage():
    db = get_db()
    user_id = session["user_id"]

    if "user_id" not in session:
        flash("You need to log in to view your profile!", "danger")
        return redirect(url_for("login"))

    # Fetch cocktails created by the logged in user 
    user_cocktails = db.execute(
        "SELECT * FROM cocktails WHERE created_by = ?", (user_id,)
    ).fetchall()

    # Fetch user's favorite cocktails by joining with cocktails table
    favorite_cocktails = db.execute("""
        SELECT c.* FROM cocktails as c
        JOIN favorites as f ON c.id = f.cocktail_id
        WHERE f.user_id = ?
    """, (user_id,)).fetchall()

    # Get the users that the logged in user is following
    followed_users = db.execute("""
        SELECT u.id, u.username 
        FROM users as u 
        JOIN follows as f ON u.id = f.following_id 
        WHERE f.follower_id = ?""", (user_id,)).fetchall()
    
    # get the cocktails created by the users that the logged in user is following
    followed_user_ids = [user['id'] for user in followed_users]
    followed_user_cocktails = []
    if followed_user_ids:
        followed_user_cocktails = db.execute("SELECT c.* FROM cocktails AS c WHERE c.created_by IN ({})".format(','.join('?' for _ in followed_user_ids)), followed_user_ids).fetchall()

    return render_template("userpage.html", user_cocktails=user_cocktails, favorite_cocktails=favorite_cocktails, followed_users=followed_users, followed_user_cocktails=followed_user_cocktails)

# Adding the cocktails to favorites
@app.route('/add_favorite/<int:cocktail_id>', methods=['POST'])
def add_favorite(cocktail_id):
    if "user_id" not in session:
        flash ("You need to log in first!", "danger")
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    db = get_db()

    # check if it already exists in favorites
    exists = db.execute(
        "SELECT favorites_id from favorites WHERE user_id = ? AND cocktail_id = ?", (user_id, cocktail_id)
    ).fetchone()
    
    if not exists:
        db.execute(
            "INSERT INTO favorites (user_id, cocktail_id) VALUES (?, ?)", (user_id, cocktail_id)
        )
        db.commit()
        flash("Added to favorites!", "success")
    else:
        flash("Already in favorites!", "warning")
    
    return redirect(url_for("explore"))  

# Removing the cocktails from favorites
@app.route('/remove_favorite/<int:cocktail_id>', methods=['POST'])  
def remove_favorite(cocktail_id):
    if "user_id" not in session:
        flash ("You need to log in first!", "danger")
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    db = get_db()

    db.execute(
        "DELETE FROM favorites WHERE user_id = ? AND cocktail_id = ?", (user_id, cocktail_id)
    )
    db.commit()
    flash("Removed from favorites!", "success")

    return redirect(url_for("userpage"))

# COMMUNITY PAGE - Displaying all the users where they can follow others
@app.route('/community.html')
def community():
    db = get_db()
    users = db.execute("SELECT id, username FROM users").fetchall()

    user_cocktails = {}
    for user in users:
        cocktails = db.execute("SELECT * FROM cocktails WHERE created_by = ?", (user['id'],)).fetchall()
        user_cocktails[user['id']] = cocktails
    
    return render_template("community.html", users=users, user_cocktails=user_cocktails)

# Follow a user
@app.route('/follow/<int:user_id>', methods=['POST'])
def follow_user(user_id):
    if "user_id" not in session:
        flash("You need to log in first!", "danger")
        return redirect(url_for("login"))
    
    db = get_db()
    current_user_id = session["user_id"]

    # # if the user is already following the other user
    existing_follow = db.execute("SELECT * FROM follows WHERE follower_id = ? AND following_id = ?",
        (current_user_id, user_id)).fetchone()

    if existing_follow:
        flash("You are already following this user!", "warning")
        return redirect(url_for("community"))
    
    # Insert the relationship into the follow database
    db.execute("INSERT INTO follows (follower_id, following_id) VALUES (?, ?)", (current_user_id, user_id))
    db.commit()

    flash("You have started following {user_id}!", "success")
    return redirect(url_for("community"))

if __name__ == '__main__':
    app.run(debug = True)
