# Task API

**FlyRank Backend Internship - Assignment 1**

---

## Overview

Task API is a simple RESTful API built using **Python** and **FastAPI** for the FlyRank Backend Internship Assignment.

It provides a RESTful interface for managing tasks using an **in-memory data store**, supporting full CRUD operations along with filtering, searching, pagination, task statistics, and resetting the seeded task list.

Since no database is used, all data exists only while the server is running.

---

## Installation & Running

### 1. Create a virtual environment (recommended)

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

Interactive Swagger documentation:

```
http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Retrieve all tasks (supports filtering, searching and pagination) |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update an existing task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/tasks/stats` | Retrieve task statistics |
| POST | `/tasks/reset` | Restore the original seeded task list |

---

## Supported Query Parameters

`GET /tasks` supports the following optional query parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `done` | Filter by completion status | `/tasks?done=true` |
| `search` | Search task titles (case-insensitive) | `/tasks?search=milk` |
| `limit` | Maximum number of tasks returned | `/tasks?limit=5` |
| `offset` | Number of tasks to skip | `/tasks?offset=5` |

Query parameters can also be combined:

```text
GET /tasks?done=true&search=milk&limit=2&offset=0
```

---

## Example cURL Request

Command

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

Example Output

```http
HTTP/1.1 201 Created
date: Sat, 18 Jul 2026 18:31:07 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

---

## Swagger Documentation

The API is fully documented using FastAPI's automatically generated Swagger UI.

![Swagger UI](images/swagger.png)

---

## Project Structure

```text
app/
├── models/
├── routes/
├── services/
├── utils/
├── data.py
└── main.py
```

The project follows a layered architecture:

- **routes/** – HTTP endpoints and request handling
- **services/** – Business logic
- **models/** – Pydantic request/response models
- **data.py** – In-memory task storage
- **utils/** – Shared helper functions (validation)

This separation keeps routing, validation and business logic independent and easier to maintain.

---

## In-Memory Persistence (Mortality Experiment)

Tasks are stored in an in-memory Python list.

This means:

- Tasks remain available while the FastAPI application is running.
- Restarting the server restores the original seeded task list.
- Any tasks created, updated or deleted during runtime are lost after the application stops.

This demonstrates the limitation of in-memory storage and highlights why persistent storage (such as a database) is required for real-world applications.

---

## Additional Features

Beyond the core CRUD functionality, the API also includes:

- Task filtering using `done`
- Case-insensitive task searching
- Pagination using `limit` and `offset`
- Task statistics endpoint
- Reset endpoint to restore seeded tasks
- Request validation with custom error responses