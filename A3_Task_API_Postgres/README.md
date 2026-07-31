# Task API

**FlyRank Backend Internship - Assignment 3**

---

## Overview

Task API is a simple RESTful API built using **Python** and **FastAPI** for the FlyRank Backend Internship Assignment.

It provides a RESTful interface for managing tasks using a **PostgreSQL database**, supporting full CRUD operations along with filtering, searching, pagination, task statistics, and resetting the seeded task list.

The application is fully containerized using **Docker** and **Docker Compose**. On startup, it automatically creates the required database schema and seeds the initial tasks if the database is empty. Task data is stored in a persistent Docker volume, allowing it to survive container restarts.


---

## Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- psycopg3
- Docker
- Docker Compose

---

## Installation & Running

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository>/A3_Task_API_Postgres
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and update the values if required:
```env
POSTGRES_DB=tasksdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Build and start the application

On first startup, PostgreSQL initializes the tasksdb database, while the application automatically creates the required tables and seeds the initial tasks if the database is empty.

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

Interactive Swagger documentation:

```
http://localhost:8000/docs
```

To stop the application:
```bash
docker compose down
```
To remove containers and database volume:
```bash
docker compose down -v
```

---

> **Development (without Docker)**

Create a virtual environment

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
### Install dependencies and run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
---

## Environment Variables


| Variable | Description |
|----------|-------------|
| POSTGRES_DB | Database name |
| POSTGRES_USER | Database username |
| POSTGRES_PASSWORD | Database password |
| POSTGRES_HOST | PostgreSQL host |
| POSTGRES_PORT | PostgreSQL port |


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
├── app/
|   ├── models/
|   ├── routes/
|   ├── services/
|   ├── utils/
|   ├── database.py
|   └── main.py
├── images/
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .dockerignore
├── .env.example
└── README.md
```

The project follows a layered architecture:

- **routes/** – HTTP endpoints and request handling
- **services/** – Business logic
- **models/** – Pydantic request/response models
- **database.py** – PostgreSQL connection management and database initialization
- **utils/** – Shared helper functions (validation)

This separation keeps routing, validation and business logic independent and easier to maintain.

---

## PostgreSQL Persistence

The application uses **PostgreSQL** as its persistence layer.

On application startup:

- The `tasks` table is created automatically if it does not already exist.
- Initial seed tasks are inserted only when the table is empty.
- Existing data is preserved across container restarts through a Docker volume.

Unlike the previous SQLite implementation, the database now runs as a dedicated PostgreSQL service managed by Docker Compose.

---

## Database

The project uses **PostgreSQL** together with the `psycopg3` driver.

All CRUD operations are performed using parameterized SQL queries to safely handle user input.

Database connection settings are configured through environment variables, making it easy to deploy the application across different environments without changing the application code.

---

## Docker

The application consists of two Docker containers managed by Docker Compose:

- **api** – FastAPI application
- **db** – PostgreSQL database

Docker Compose automatically creates an isolated network allowing the FastAPI application to communicate with the PostgreSQL container using the configured service name.

The services communicate over Docker's internal network, while a named Docker volume is used to persist database data across container restarts.

---

## Additional Features

Beyond the core CRUD functionality, the API also includes:

- PostgreSQL-based persistent storage
- Dockerized application deployment
- Docker Compose orchestration
- Environment-based configuration
- Automatic database initialization and seeding
- Task filtering using `done`
- Case-insensitive task searching
- Pagination using `limit` and `offset`
- Task statistics endpoint
- Reset endpoint to restore seeded tasks
- Request validation with custom error responses
- Interactive Swagger/OpenAPI documentation

---

## Assignment 3 Changes

Compared to Assignment 2, the following improvements were made:

- Migrated the persistence layer from SQLite to PostgreSQL.
- Replaced the `sqlite3` module with the `psycopg3` PostgreSQL driver.
- Externalized database configuration using environment variables.
- Containerized the FastAPI application using Docker.
- Added Docker Compose for multi-container orchestration.
- Configured persistent PostgreSQL storage using Docker volumes.
- Preserved the existing REST API contract and endpoint behavior.

---
## Inspecting the Database

The PostgreSQL database can be inspected using tools such as:

- psql
- pgAdmin
- VS Code PostgreSQL extensions

The running PostgreSQL container can also be accessed directly using:

```bash
docker exec -it taskdb psql -U postgres -d tasksdb
```
After entering the PostgreSQL shell, common commands include:
```sql
\dt
SELECT * FROM tasks;
```