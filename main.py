from fastapi import FastAPI, status, HTTPException, Depends
from dotenv import load_dotenv
import bcrypt
# from sqlalchemy.orm import Session
from .models import RegisterUser, Tasks
from .database import get_db, init_db
from sqlmodel import Session, select

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




# # Retrieve a task by id 
# @app.get('/tasks/{id}', status_code=status.HTTP_200_OK)
# async def retrieve_all_tasks(id: int):
#     cursor.execute (""" SELECT * FROM tasks WHERE id=%s""", (id,))
#     a_task = cursor.fetchone()
#     if not a_task:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id '{id}' not found")
#     conn.commit()
#     print(a_task)

#     return {"respons": a_task}


# # Deleting a Task
# @app.delete('/tasks/{id}', status_code=status.HTTP_200_OK)
# async def delete_post(id: int):
#     cursor.execute(""" DELETE FROM tasks WHERE id=%s returning * """, (id,))
#     d_task = cursor.fetchone()
#     conn.commit()
#     if d_task == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with iD of '{id}' not found")
    
#     return{"data", d_task}


# # Updating a Task
# @app.put('/tasks/{id}', status_code=status.HTTP_200_OK)
# async def update_task(id: int, new_task: Tasks):
#     cursor.execute(""" UPDATE tasks SET title = %s, description = %s, dueDate = %s, status = %s, createdAt = %s, updatedAt = %s WHERE id = %s RETURNING * """,( new_task.title, new_task.description, new_task.dueDate, new_task.status, new_task.createdAt, new_task.updatedAt, id))
#     updated_task = cursor.fetchone()
#     conn.commit()

#     if updated_task == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with iD of '{id}' not found")
    
#     return{"data": updated_task}


if __name__ == "__main__":
    init_db()