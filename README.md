# AI Learning Management Platform

## Project

I am building an AI Learning Management Platform using FastAPI for the backend and React for the frontend.

The application is for companies to manage employee learning. Employees can enroll in courses, track their progress, and improve their skills. I will also add AI features like course recommendations and skill gap analysis.

## Technologies

- FastAPI
- React
- PostgreSQL
- SQLAlchemy
- Git & GitHub
- JWT Authentication
- Passlib (Password Hashing)
- Python-JOSE

## Folder Structure

```
backend/
frontend/
docs/
prompts/
README.md
```

## Current Progress

- Created the GitHub repository
- Set up the project folders
- Planned the database
- Created the ER diagram
- Started the backend setup
- Connected PostgreSQL database
- Created SQLAlchemy models
- Created all database tables
- Implemented user registration
- Implemented secure password hashing
- Implemented user login
- Generated JWT access tokens
- Protected authenticated routes
- Implemented role-based authorization
- Tested APIs using Swagger UI

## Features Implemented

### Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing using bcrypt
- Protected API Endpoints
- Current User API (`/auth/me`)
- Role-Based Authorization (Admin/User)

### Database

- PostgreSQL Integration
- SQLAlchemy ORM Models
- User Table
- Course Table
- Lesson Table
- Enrollment Table
- Skill Table
- Employee Skill Table
- Certificate Table
- Learning Path Table
- AI Recommendation Table

### API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/me` | Get current authenticated user |
| GET | `/auth/admin` | Admin-only protected endpoint |

## Next Steps

- Build authentication
- Connect PostgreSQL
- Create APIs
- Build the frontend
- Course Management APIs
- Lesson Management APIs
- Enrollment APIs
- Certificate Generation
- AI Course Recommendation
- Skill Gap Analysis
- Employee Dashboard
- Admin Dashboard

## How to Run

### Clone the Repository

```bash
git clone <repository-url>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### macOS/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### Swagger Documentation

```
http://127.0.0.1:8000/docs
```

## Author

Shaik Sohel