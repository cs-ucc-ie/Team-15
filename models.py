
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class YourTable(Base):
    __tablename__ = 'your_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Add other columns as needed

# Load database 
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('db.db')

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
