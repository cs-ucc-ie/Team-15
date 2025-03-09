import sqlite3
import os
import openai
from flask import Flask, request, redirect, url_for, render_template, g, session, flash, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date
from sqlalchemy.orm import scoped_session
from models import Session  
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  


app.secret_key = "my_secret_key"
CORS(app)

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# OpenAI API Setup
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is not set. Check your .env file.")

openai.api_key = OPENAI_API_KEY

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

# Session for SQLAlchemy
db_session = scoped_session(Session)

@app.route('/chat.html')
def chat_page():
    return render_template('chat.html')

@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    data = request.json
    user_id = data.get('user_id')
    favorite_ingredients = ','.join(data.get('favorite_ingredients', []))
    disliked_ingredients = ','.join(data.get('disliked_ingredients', []))
    preferred_cocktail_types = ','.join(data.get('preferred_cocktail_types', []))

    user_pref = UserPreferences.query.filter_by(user_id=user_id).first()

    if user_pref:
        user_pref.favorite_ingredients = favorite_ingredients
        user_pref.disliked_ingredients = disliked_ingredients
        user_pref.preferred_cocktail_types = preferred_cocktail_types
    else:
        user_pref = UserPreferences(user_id, favorite_ingredients, disliked_ingredients, preferred_cocktail_types)
        db.session.add(user_pref)

    db.session.commit()
    return jsonify({"message": "Preferences saved successfully!"}), 200


@app.route('/get_preferences/<int:user_id>', methods=['GET'])
def get_preferences(user_id):
    user_pref = UserPreferences.query.filter_by(user_id=user_id).first()
    
    if not user_pref:
        return jsonify({"message": "No preferences found!"}), 404
    
    return jsonify({
        "user_id": user_pref.user_id,
        "favorite_ingredients": user_pref.favorite_ingredients.split(','),
        "disliked_ingredients": user_pref.disliked_ingredients.split(','),
        "preferred_cocktail_types": user_pref.preferred_cocktail_types.split(',')
    }), 200


# AI Chatbox Route
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == "GET":
        # Fetch cocktails from the database
        db_data = Cocktails.query.all()
        cocktail_list = [{"name": item.name} for item in db_data]
        return jsonify({"cocktails": cocktail_list})

    # Handle POST request (AI chat)
    data = request.json
    user_id = data.get("user_id")
    user_input = data.get("message", "")

    # Fetch cocktail names from the database
    db_data = db.session.query(Cocktails).all()
    cocktail_list = [item.name for item in db_data]

    if not cocktail_list:
        # If no cocktails are found, generate them dynamically using GPT-4
        prompt = f"""
        You are an expert mixologist. The user is asking for cocktail recommendations.
        Since no cocktails are available in the database, create a new and unique cocktail recipe.
        
        User request: {user_input}

        Respond with:
        - A unique cocktail name
        - List of ingredients
        - Step-by-step instructions
        - Optional garnish or serving suggestions.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant specializing in cocktail recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        return jsonify({"response": response.choices[0].message.content.strip()}), 200

    # Convert the cocktail list to a string for the AI
    data_str = '\n'.join(cocktail_list) if cocktail_list else "No cocktails available."

    # Fetch user preferences
    user_pref = UserPreferences.query.filter_by(user_id=user_id).first()
    preference_prompt = ""

    if user_pref:
        preference_prompt = f"""
        The user prefers cocktails with {user_pref.favorite_ingredients}.
        They dislike {user_pref.disliked_ingredients}.
        They enjoy {user_pref.preferred_cocktail_types} cocktails.
        """

    # Final AI prompt with user preferences
    prompt = f"""
    {preference_prompt}
    You are a cocktail expert. Recommend a cocktail from the list below based on the user's request.

    Available Cocktails:
    {data_str}

    User: {user_input}
    AI:
    """

    # Generate recommendation using GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant specializing in cocktail recommendations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return jsonify({"response": response.choices[0].message.content.strip()}), 200




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

@app.route('/login.html', methods=['GET', 'POST'])
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

"""@app.route('/pantry.html', methods=['GET'])
def pantry():
    db = get_db()
    ingredients = db.execute("SELECT * FROM ingredients").fetchall()
    return render_template("pantry.html", ingredients=ingredients)"""

@app.route('/pantry.html', methods=['GET'])
def pantry():
    db = get_db()
    ingredients = db.execute("SELECT * FROM ingredients").fetchall()

    matching_cocktails = db.execute("""
        SELECT DISTINCT c.id, c.name 
        FROM cocktails c
        JOIN cocktail_ingredients ci ON c.id = ci.cocktail_id
    """).fetchall()

    return render_template("pantry.html", ingredients=ingredients, matching_cocktails=matching_cocktails)


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

# User Profile Page, displaying the cocktails created by the user and the favorite cocktails
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

@app.route('/edit_cocktail', methods=['POST'])
def edit_cocktail():
    db = get_db()
    cocktail_id = request.form['cocktail_id']
    name = request.form['name']
    alcohol_content = int(request.form['alcohol_content'])
    method = request.form['method']

    image = request.files['image']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        db.execute(
            "UPDATE cocktails SET name = ?, alcohol_content = ?, method = ?, image = ? WHERE id = ?",
            (name, alcohol_content, method, filename, cocktail_id)
        )
    else:
        db.execute(
            "UPDATE cocktails SET name = ?, alcohol_content = ?, method = ? WHERE id = ?",
            (name, alcohol_content, method, cocktail_id)
        )

    db.commit()
    flash("Cocktail updated successfully!", "success")
    return redirect(url_for('userpage'))

@app.route('/get_cocktail/<int:cocktail_id>')
def get_cocktail(cocktail_id):
    db = get_db()
    cocktail = db.execute("SELECT * FROM cocktails WHERE id = ?", (cocktail_id,)).fetchone()
    
    if cocktail:
        return jsonify({
            'id': cocktail['id'],
            'name': cocktail['name'],
            'alcohol_content': cocktail['alcohol_content'],
            'method': cocktail['method']
        })
    return jsonify({'error': 'Cocktail not found'}), 404

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
