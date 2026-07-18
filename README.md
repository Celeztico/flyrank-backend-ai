# FlyRank Backend Internship Assignments

This repository contains my solutions for the **FlyRank Backend Internship** weekly assignments.

The goal of these assignments is to build backend systems while following clean architecture, REST API design principles, and industry-standard development practices using **Python** and **FastAPI**.

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
├── A2_...
│
└── README.md
```

Each assignment is self-contained and includes its own source code, documentation, and instructions for running the project.

---

## Assignments

| Assignment | Description | Status |
|------------|-------------|--------|
| **A1 - Task API** | RESTful CRUD Task Management API built with FastAPI using an in-memory data store. | ✅ Completed |
| **A2 - ...** | Coming soon | ⏳ |
| **A3 - ...** | Coming soon | ⏳ |

---

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Git & GitHub

---

## Highlights

Throughout these assignments I aim to follow common backend development practices, including:

- Modular project structure
- Separation of concerns (Routes → Services → Models)
- RESTful API design
- Request validation
- Proper HTTP status codes
- Swagger/OpenAPI documentation
- Meaningful Git commits

---

## Running an Assignment

Each assignment contains its own README with setup instructions.

For example:

```bash
cd A1_Task_API
pip install -r requirements.txt
uvicorn app.main:app --reload
```
