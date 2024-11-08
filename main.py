from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import uuid4, UUID
from datetime import datetime, timezone


app = FastAPI()

# User model
class RegisterUser(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    username: Optional[str] = True
    password: str


# Task model
class Tasks(BaseModel):
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
    print(new_user)
    return {"response": "Registeration successfull"}


@app.post("/tasks")
async def create_task(new_task: Tasks):
    print(new_task)
    return {"response": "new task created."}