from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db = SQLAlchemy()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///site.db")  # Default to SQLite if not set
engine = create_engine(DATABASE_URL)

# Create session factory
Session = sessionmaker(bind=engine)
session = scoped_session(Session)  # Define scoped session

# Define Models
class Cocktails(db.Model):
    __tablename__ = 'cocktails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    favorite_ingredients = db.Column(db.Text, nullable=True)
    disliked_ingredients = db.Column(db.Text, nullable=True)
    preferred_cocktail_types = db.Column(db.Text, nullable=True)

# Initialize Database
def init_db():
    db.create_all()
