# TaskFlow API

Production-ready Task Management REST API built with FastAPI.

---

## Overview

TaskFlow API is a backend project developed to practice real-world backend engineering concepts using FastAPI and PostgreSQL.

This project focuses on:
- scalable API architecture
- authentication & authorization
- async backend development
- Docker containerization
- automated testing
- CI/CD workflow

The goal of this project is to simulate a production-ready backend system instead of a simple CRUD tutorial application.

---

## Features

- JWT Authentication
- User Registration & Login
- Task CRUD Management
- Protected API Routes
- PostgreSQL Integration
- SQLAlchemy ORM
- Async FastAPI Architecture
- Docker Support
- Automated Testing with Pytest
- CI/CD with GitHub Actions
- Environment Variable Management

---

## Tech Stack

### Backend
- Python
- FastAPI
- Pydantic

### Database
- PostgreSQL
- SQLAlchemy
- Alembic

### DevOps & Tools
- Docker
- GitHub Actions
- Railway

### Testing
- Pytest

---

## Project Structure

```bash
taskflow-api-fastapi/
│
├── .github/workflows/     # GitHub Actions CI/CD workflows
├── alembic/               # Database migrations
├── controllers/           # Handle API request logic
├── core/                  # Security, config, JWT settings
├── db/                    # Database connection & session
├── dependencies/          # FastAPI dependencies
├── exceptions/            # Custom exception classes
├── handlers/              # Global exception handlers
├── middleware/            # Custom middleware
├── models/                # SQLAlchemy database models
├── repositories/          # Database query layer
├── schemas/               # Pydantic request/response schemas
├── services/              # Business logic layer
├── tests/                 # Unit and integration tests
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── explain-folders.txt
├── main.py                # FastAPI application entry point
├── requirements.txt
├── start.sh               # Application startup script
└── README.md
```

---

## Architecture

The project follows a clean layered architecture:

- **Routes Layer**
  - Handles HTTP requests and responses

- **Service Layer**
  - Contains business logic

- **Repository Layer**
  - Handles database operations

- **Models Layer**
  - Defines database structure

- **Schemas Layer**
  - Validates request and response data

### Benefits
- Better scalability
- Easier maintenance
- Cleaner code separation
- Improved testability

---

## Authentication

This project uses JWT Authentication.

### Security Features
- Password Hashing
- JWT Access Token
- Protected Routes
- User Authorization

---

## Installation

### Clone Repository

```bash
git clone https://github.com/joshhanson02/taskflow-api-fastapi.git
cd taskflow-api-fastapi
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Run the Application

```bash
uvicorn main:app --reload
```

Application will run at:

```bash
http://127.0.0.1:8000
```

---

## API Documentation

Swagger UI:

```bash
http://127.0.0.1:8000/docs
```

Production API Docs:

```bash
https://taskflowapifastapi.up.railway.app/docs
```

---

## Docker Setup

### Build and Run

```bash
docker compose up --build
```

### Run in Background

```bash
docker compose up -d
```

---

## Testing

Run unit tests:

```bash
pytest
```

The project includes tests for:
- authentication
- task CRUD operations
- validation
- protected routes

---

## CI/CD

GitHub Actions automatically:
- install dependencies
- run unit tests
- validate project on every push

---

## Deployment

The application is deployed using:
- Railway
- Docker
- PostgreSQL

---

## Future Improvements

- Redis Caching
- Background Jobs
- Celery Integration
- Role-Based Access Control (RBAC)
- Rate Limiting
- Logging & Monitoring
- Refresh Token Authentication
- API Versioning

---

## Author

Tran Nguyen Trung Hieu

- GitHub: https://github.com/joshhanson02
- LinkedIn: https://linkedin.com/in/joshhanson02

```
