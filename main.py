from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import uuid4, UUID
from datetime import datetime, timezone
import psycopg

from dotenv import load_dotenv
import os
import bcrypt
import time


load_dotenv()

app = FastAPI()

db_host = os.getenv("HOST")
db_databse = os.getenv("DATABASE")
db_user = os.getenv("USER")
db_password = os.getenv("PASSWORD")
db_port = os.getenv("PORT")



# Connectinng to the database
while True:
    try:
        conn = psycopg.connect(dbname=db_databse, user=db_user, password=db_password,host=db_host, port=db_port)
        cursor = conn.cursor()
            # SQL to create the users table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            username VARCHAR(50) UNIQUE NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        create_task_sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(50) NOT NULL,
            dueDate DATE,
            status VARCHAR(255) NOT NULL,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """


        # Execute the table creation
        cursor.execute(create_table_sql)
        cursor.execute(create_task_sql)
        conn.commit()
        print("Users Table created successfully 🎉🎉🎉")
        print("Task Table created successfully 🎉🎉🎉")
        print("Database connection, successful 🎉🎉🎉")
        break
    except Exception as err:
        print("Connecting to Database failed")
        print("Error message is:", err)
        time.sleep(3)


# User model
class RegisterUser(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    username: Optional[str] = True
    password: str


# Task model
class Tasks(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    dueDate: datetime
    status: Literal["pending", "in-progress", "completed."]
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@app.get("/")
async def home_view():
    return {"home": "Welcome to our Homepage"}


@app.post("/users/register/")
async def register_view(new_user: RegisterUser):
    # Hashing the password
    new_password = new_user.password
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    cursor.execute(""" INSERT INTO users (email, username, password) VALUES (%s,%s,%s) RETURNING * """, (new_user.email, new_user.username, hashed_password.decode("utf-8")))
    registerd_users = cursor.fetchone()
    conn.commit() # For your data to be showing in your database table you must commit it and not to be refrenced to cursor but to conn.
    print(registerd_users)
    return {"response": "Registeration successfull"}

# Creating a new task
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(new_task: Tasks):
    cursor.execute(""" INSERT INTO tasks (title, description, dueDate, status, createdAt, updatedAt) VALUES (%s,%s,%s,%s,%s,%s) RETURNING * """, (new_task.title, new_task.description, new_task.dueDate, new_task.status, new_task.createdAt, new_task.updatedAt))
    new_tasks = cursor.fetchone()
    conn.commit()
    print(new_tasks)
    return {"data": new_tasks}


# Retrieve all tasks with pagination 
@app.get('/tasks', status_code=status.HTTP_200_OK)
async def retrieve_all_tasks():
    cursor.execute (""" SELECT * FROM tasks""")
    all_tasks = cursor.fetchall()
    if not all_tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task found")
    conn.commit()
    print(all_tasks)

    return {"data": all_tasks}


# Retrieve a task by id 
@app.get('/tasks/{id}', status_code=status.HTTP_200_OK)
async def retrieve_all_tasks(id: int):
    cursor.execute (""" SELECT * FROM tasks WHERE id=%s""", (id,))
    a_task = cursor.fetchone()
    if not a_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id '{id}' not found")
    conn.commit()
    print(a_task)

    return {"respons": a_task}


# Deleting a Task
@app.delete('/tasks/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM tasks WHERE id=%s returning * """, (id,))
    d_task = cursor.fetchone()
    conn.commit()
    if d_task == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Task with iD of '{id}' not found")
    
    return{"data", d_task}