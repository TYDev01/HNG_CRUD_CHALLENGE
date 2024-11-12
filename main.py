from fastapi import FastAPI, status, HTTPException, Depends
from dotenv import load_dotenv
import bcrypt
# from sqlalchemy.orm import Session
from .models import RegisterUser, Tasks
from .database import get_db, init_db
from sqlmodel import Session, select
from datetime import datetime

init_db()
load_dotenv()
app = FastAPI()



# Task model
# class Tasks(BaseModel):
#     id: UUID = Field(default_factory=uuid4)
#     title: str
#     description: str
#     dueDate: datetime
#     status: Literal["pending", "in-progress", "completed."]
#     createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
#     updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@app.get("/")
async def home_view():
    return {"home": "Welcome to our Homepage"}


@app.post("/users/register/")
async def register_view(new_user: RegisterUser, db: Session = Depends(get_db)):
    # Hashing the password
    new_password = new_user.password
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user.password = hashed_password #Replacing the plain password to the hashed password.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return {"response": "Registeration successfull"}

# # Login a user
# @app.post("/users/login/")
# async def login_user():
#     cursor.execute("""
#     SELECT * FROM users
# """)

# Creating a new task
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(new_task: Tasks, db: Session = Depends(get_db)):
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    # print(new_task)
    return {"data": new_task}


# # Retrieve all tasks with pagination 
@app.get('/tasks', status_code=status.HTTP_200_OK)
async def retrieve_all_tasks(page: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = select(Tasks).offset(page).limit(limit)
    all_tasks = db.exec(query)
    tasks = all_tasks.fetchall()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task found")
    print(tasks)

    return {"data": tasks}




# Retrieve a task by id 
@app.get('/tasks/{id}', status_code=status.HTTP_200_OK)
async def retrieve_all_tasks(id: int, db: Session = Depends(get_db)):
    task = db.get(Tasks, id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id '{id}' not found")
    print(task)

    return {"respons": task}


# Deleting a Task
@app.delete('/tasks/{id}', status_code=status.HTTP_200_OK)
async def delete_post(id: int, db: Session = Depends(get_db)):
    get_task_first = db.get(Tasks, id)
    if get_task_first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with iD of '{id}' not found")
    d_task = db.delete(get_task_first)
    db.commit()
    
    return{ "Deleted Successfully"}


# Updating a Task
@app.put('/tasks/{id}', status_code=status.HTTP_200_OK)
async def update_task(id: int, unew_task: Tasks, db: Session = Depends(get_db)):
    task_to_be_updated = db.get(Tasks, id)
    print(task_to_be_updated)
    if task_to_be_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with iD of '{id}' not found")
    task_to_be_updated.title = unew_task.title
    task_to_be_updated.description = unew_task.description
    task_to_be_updated.dueDate = unew_task.dueDate
    task_to_be_updated.status = unew_task.status
    task_to_be_updated.updatedAt = datetime.now()

    db.add(task_to_be_updated)
    db.commit()
    db.refresh(task_to_be_updated)
    
    return{"data": task_to_be_updated}


