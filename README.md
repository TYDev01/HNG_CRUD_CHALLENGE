# FastAPI Task Management Application

## Overview

This is a FastAPI-based task management application that allows users to register and manage tasks with CRUD (Create, Read, Update, Delete) functionality. The application supports user registration with hashed passwords and tasks with statuses such as "pending," "in-progress," and "completed."

---

## Features

1. **User Registration**:
   - Registers users with hashed passwords for security.
   - Ensures uniqueness of email and username during registration.

2. **Task Management**:
   - **Create Tasks**: Add new tasks with title, description, due date, and status.
   - **Retrieve Tasks**: Fetch all tasks with pagination support or retrieve a task by its ID.
   - **Update Tasks**: Modify task details, including title, description, due date, and status.
   - **Delete Tasks**: Remove a task by its ID.

3. **Homepage**:
   - Provides a simple welcome message at the root endpoint.

---

## Endpoints

### **Home**
- **GET** `/`
  - **Response**: A welcome message.

---

### **User Registration**
- **POST** `/users/register/`
  - **Request Body**:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string"
    }
    ```
  - **Response**:
    - Success: `"Registration successful"`
    - Error: `HTTP 400 - Email or Username already registered`

---

### **Task Endpoints**

#### **Create a Task**
- **POST** `/tasks`
  - **Request Body**:
    ```json
    {
      "title": "string",
      "description": "string",
      "dueDate": "datetime",
      "status": "pending | in-progress | completed"
    }
    ```
  - **Response**:
    - Success: Task data with HTTP 201.
    - Error: `HTTP 400` for validation issues.

---

#### **Retrieve All Tasks**
- **GET** `/tasks`
  - **Query Parameters**:
    - `page` (default: 0)
    - `limit` (default: 10)
  - **Response**:
    - Success: List of tasks with pagination.
    - Error: `HTTP 404` if no tasks found.

---

#### **Retrieve a Task by ID**
- **GET** `/tasks/{id}`
  - **Path Parameter**:
    - `id`: Task ID (integer)
  - **Response**:
    - Success: Task data.
    - Error: `HTTP 404` if task not found.

---

#### **Update a Task**
- **PUT** `/tasks/{id}`
  - **Path Parameter**:
    - `id`: Task ID (integer)
  - **Request Body**:
    ```json
    {
      "title": "string",
      "description": "string",
      "dueDate": "datetime",
      "status": "pending | in-progress | completed"
    }
    ```
  - **Response**:
    - Success: Updated task data.
    - Error: `HTTP 404` if task not found.

---

#### **Delete a Task**
- **DELETE** `/tasks/{id}`
  - **Path Parameter**:
    - `id`: Task ID (integer)
  - **Response**:
    - Success: `"Deleted Successfully"`
    - Error: `HTTP 404` if task not found.

---

## Setup Instructions

### Prerequisites
1. Python 3.9 or later
2. Dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TYDev01/HNG_CRUD_CHALLENGE.git
   cd <repository-folder>

<hr>
pip install -r requirements.txt

<hr>

### Configure the environment variables:
Create a .env file and set the necessary database connection details.
1. Initialize the database:
    ```bash
    from .database import init_db
    init_db()

<hr>

### Start the FastAPI server:
1. Starting the server
    ```bash
    fastapi dev main.py

