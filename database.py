from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
print(f"DATABASE_URL: {DATABASE_URL}")
# print(engine.url)

# print("test")

# Dependency, it's responsible for  talking with the database. 
def init_db():
    print("Test")
    try:
        SQLModel.metadata.create_all(engine)
        print("Database created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")


def get_db():
    with Session(engine) as session:
        yield session # Get a session anytime we talk to the database.
