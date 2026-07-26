# AI Learning Management Platform

## Overview

The AI Learning Management Platform is a full-stack web application built using **FastAPI**, **React**, and **PostgreSQL**. It enables organizations to securely manage employee learning through authentication, role-based access control, and complete course management.

The project follows a clean service-layer architecture and demonstrates full-stack development with a REST API backend and a React frontend.

---

# Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing (bcrypt)
- Protected API Endpoints
- Current User API (`/auth/me`)
- Role-Based Authorization (Admin/User)

---

## Course Management

- Create Course
- View Courses
- Update Course
- Delete Course

---

## Search & Filtering

- Search Courses by Title
- Filter by Category
- Filter by Difficulty
- Sort by Title
- Sort by Duration
- Sort by Difficulty
- Pagination

---

## Validation

### Backend

- Pydantic Validation
- Duplicate Course Prevention
- Secure API Validation

### Frontend

- Client-side Form Validation
- Required Field Validation
- Error Messages

---

# Technologies Used

## Frontend

- React
- React Router
- Axios
- CSS

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT Authentication
- Passlib (bcrypt)
- Python-JOSE

## Tools

- Git
- GitHub
- Swagger UI
- VS Code

---

# Project Structure

```
ai-learning-management-platform/

├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docs/
├── prompts/
└── README.md
```

---

# Implemented Features

## Authentication APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/me` | Get authenticated user |
| GET | `/auth/admin` | Admin-only endpoint |

---

## Course APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/courses` | Create Course |
| GET | `/courses` | Get All Courses |
| GET | `/courses/{id}` | Get Course by ID |
| PUT | `/courses/{id}` | Update Course |
| DELETE | `/courses/{id}` | Delete Course |

---

# Current Progress

- GitHub Repository Created
- FastAPI Backend Setup
- PostgreSQL Database Connected
- SQLAlchemy Models Created
- JWT Authentication Implemented
- Role-Based Authorization Added
- User Registration & Login Completed
- Course CRUD APIs Completed
- Search Functionality Added
- Category Filtering Added
- Difficulty Filtering Added
- Sorting Implemented
- Pagination Implemented
- React Frontend Integrated
- Protected React Routes Added
- Context API for Authentication
- Axios API Integration
- Responsive UI
- Client-side Validation
- Backend Validation
- Swagger API Testing Completed

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

---

## Backend Setup

```bash
cd backend

python -m venv venv
```

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# Future Enhancements

- Employee Course Enrollment
- Lesson Management
- Course Progress Tracking
- Certificate Generation
- AI Course Recommendation
- Skill Gap Analysis
- Learning Paths
- Employee Dashboard
- Admin Analytics Dashboard
- Email Notifications

---

# Author

**Sohel Shaik**