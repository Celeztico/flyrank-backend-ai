# FlyRank Backend Internship Assignments

This repository contains my solutions for the **FlyRank Backend Internship** weekly assignments.

The goal of these assignments is to progressively build backend systems while following layered architecture, REST API design principles, database integration, containerization, and industry-standard development practices using Python and FastAPI.

---

## Repository Structure

```text
.
├── A1_Task_API/
│   ├── app/
│   ├── images/
│   ├── README.md
│   └── requirements.txt
│
├── A2_Task_API_DB/
│   ├── app/
│   ├── images/
│   ├── README.md
│   └── requirements.txt
│
├── A3_Task_API_Postgres/
│   ├── app/
│   ├── images/
│   ├── Dockerfile
│   ├── compose.yaml
│   ├── README.md
│   └── requirements.txt
|
├── A4_Task_API_Auth/
│   ├── app/
│   ├── images/
│   ├── Dockerfile
│   ├── compose.yaml
│   ├── README.md
│   └── requirements.txt
│
└── README.md
```

Each assignment is self-contained and includes its own source code, documentation, and instructions for running the project.

---

## Assignments

| Assignment | Description | Status |
|------------|-------------|--------|
| **A1 - Task API** | RESTful CRUD Task Management API built with FastAPI using an in-memory data store. | ✅ Completed |
| **A2 - Task API with DB** | RESTful CRUD Task Management API built with FastAPI migrated to use an sqlite database. | ✅ Completed |
| **A3 - Task API with PostgreSQL & Docker** | Migrated the Task API to PostgreSQL and containerized the application using Docker and Docker Compose. | ✅ Completed |
| **A4 - Task API with Supabase Auth** | Updated the Task API to use Supabase Authentication and JWT tokens | ✅ Completed |
| **A5 - ...** | Coming soon | ⏳ |

---

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- SQLite
- PostgreSQL
- psycopg3
- Docker
- Docker Compose
- Git & GitHub

---

## Highlights

Throughout these assignments I aim to follow common backend development practices, including:

- Modular project structure
- Layered architecture (Routes → Services → Models)
- RESTful API design
- Request validation
- Proper HTTP status codes
- SQL-based persistence
- Dockerized deployment
- Environment-based configuration
- Swagger/OpenAPI documentation
- Meaningful Git commits

---

## Running an Assignment

Each assignment contains its own README with setup instructions.

For example:
**Assignment 1**
```bash
cd A1_Task_API
pip install -r requirements.txt
uvicorn app.main:app --reload
```
