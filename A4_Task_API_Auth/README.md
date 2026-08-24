# Task API with Supabase Authentication

**FlyRank Backend Internship - Assignment 4**

---

## Overview

Task API is a RESTful API built using **Python** and **FastAPI** for the FlyRank Backend Internship Assignment.

It provides a RESTful interface for managing tasks using a **PostgreSQL database**, supporting full CRUD operations along with filtering, searching, pagination, task statistics, and resetting the seeded task list.

The API now includes **Supabase Authentication** with email/password signup and login, JWT-based authentication for protected endpoints, and logout functionality.

The application is fully containerized using **Docker** and **Docker Compose**. PostgreSQL data is stored in a persistent Docker volume, allowing task data to survive container restarts.


---

## Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- psycopg3
- Supabase Auth
- Docker
- Docker Compose

---

## Installation & Running

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository>/A4_Task_API_Postgres
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and update the values if required:
```env
POSTGRES_DB=tasksdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

SUPABASE_URL=https://<your-project-ref>.supabase.co
SUPABASE_KEY=<your-supabase-key>
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
> Removing the volume deletes the persisted PostgreSQL task data.
---

> **Development (without Docker)**

Docker Compose is the recommended way to run the complete application.

For development, the FastAPI application can also be run directly while keeping PostgreSQL running in Docker.

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
```
When running FastAPI outside Docker, PostgreSQL must be reachable from the host machine. For example:
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
Run the application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
> --host 0.0.0.0 is optional and only needs to be done if the app has to be accessible to any device on local network
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

## Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|---------|----------|-------------|----------------|
| POST | `/auth/signup` | Register a new user | Public |
| POST | `/auth/login` | Authenticate a user and obtain tokens | Public |
| POST | `/auth/logout` | Logout the current Supabase session | Pubic |

### Signup
```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```
Successful signup returns:
```http
HTTP/1.1 201 Created
```
Missing credentials or invalid signup input returns:
```http
HTTP/1.1 400 Bad Request
```

### Login
```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```
Successful login returns:
```json
{
  "access_token": "<access-token>",
  "refresh_token": "<refresh-token>"
}
```
Invalid credentials returns:
```http
HTTP/1.1 401 Unauthorized
```

### Logout
```bash
curl -i -X POST http://localhost:8000/auth/logout
```
Successful logout returns:
```http
HTTP/1.1 200 OK
```

---

## API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/public/info` | Public information endpoint |
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Authenticate a user and obtain tokens |
| POST | `/auth/logout` | Logout the current Supabase session |

### Protected Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/protected/profile` | Retrieve the authenticated user's ID and email |
| GET | `/protected/dashboard` | Protected dashboard endpoint |
| GET | `/tasks` | Retrieve all tasks (supports filtering, searching and pagination) |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update an existing task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/tasks/stats` | Retrieve task statistics |
| POST | `/tasks/reset` | Restore the original seeded task list |

Request to protected endpoints must include:
```http
Authorization: Bearer <access_token>
```

Requests without a token or with an invalid/expired token return:
```http
401 Unauthorized
```
---

## Protected Request Example

After logging in, use the returned `access_token`
```bash
curl -i http://localhost:8000/tasks \
  -H "Authorization: Bearer <access_token>"
```

Example successful response:
```http
HTTP/1.1 200 OK
```

Without authentication:
```bash
curl -i http://localhost:8000/tasks
```
Expected:
```http
HTTP/1.1 401 Unauthorized
```

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
Remember that the request must include a valid access token
---

## Example cURL Request

Command

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
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
The protected endpoint use Bearer authentication.
A valid access token can be supplied through Swagger's Authorize functionality and then used when testing protected endpoints

![Swagger UI](images/swagger.png)

---

## Project Structure

```text
├── app/
|   ├── auth/
|   |   ├── client.py
|   |   ├── dependencies.py
|   |   ├── router.py
|   |   ├── schemas.py
|   |   └── service.py
|   ├── models/
|   ├── routes/
|   |   ├── public.py
|   |   ├── protected.py
|   |   └── tasks.py
|   ├── services/
|   ├── utils/
|   ├── config.py
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

- **auth/** – Supabase authentication, authentication services, token verification, and reusable authentication dependencies
- **routes/** – HTTP endpoints and request handling
- **services/** – Task Business logic and database operations
- **models/** – Pydantic request/response models
- **database.py** – PostgreSQL connection management and database initialization
- **config.py** - Environment-based application configuration
- **utils/** – Shared helper functions (validation)

This separation keeps routing, validation and business logic independent and easier to maintain.

The reusable `get_current_user()` dependency centralizes access-token verification and is used to protect authenticated routes.

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

Authentication data is managed by Supabase rather than stored in the application's PostgreSQL task database.

---

## Docker

The application consists of two Docker services managed by Docker Compose:

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
- Supabase email/password authentication
- JWT access-token verification
- Protected routes using FastAPI dependencies
- Public and protected endpoint separation
- Task filtering using `done`
- Case-insensitive task searching
- Pagination using `limit` and `offset`
- Task statistics endpoint
- Reset endpoint to restore seeded tasks
- Request validation with custom error responses
- Interactive Swagger/OpenAPI documentation
- Bearer-token authentication in Swagger

---

## Assignment 4 Changes

Compared to Assignment 3, the following improvements were made:

 - Added Supabase Auth for user registration and authentication.
 - Added email/password signup through `/auth/signup`.
 - Added login through `/auth/login`.
 - Added logout through `/auth/logout`.
 - Added JWT access-token verification using Supabase.
 - Added reusable `get_current_user()` authentication dependency.
 - Added public and protected route groups.
 - Protected the Task API using authenticated access.
 - Added authenticated user information to `/protected/profile`.
 - Added protected dashboard endpoint.
 - Preserved the existing Task API functionality and PostgreSQL persistence.
 - Added authentication configuration through environment variables.
 - Updated Swagger/OpenAPI documentation to support Bearer authentication.

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