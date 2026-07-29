# REST API Documentation

The backend of the AI Learning Management Platform is powered by **FastAPI**, offering fully typed, auto-documented REST endpoints.

> [!TIP]
> **Swagger UI**: When running the backend locally, navigate to `http://localhost:8000/docs` to view the interactive Swagger UI and test endpoints directly from the browser.

---

## 🔒 Authentication Guidelines

All protected endpoints require a **Bearer Token** in the `Authorization` header.

```http
Authorization: Bearer <your_jwt_token_here>
```

Tokens are obtained via the `/auth/login` endpoint.

---

## 🧑‍💻 Auth Endpoints

### 1. Register User
Creates a new user profile.

- **Method**: `POST`
- **Path**: `/auth/register`
- **Auth Required**: No

**Request Body**:
```json
{
  "name": "Jane Doe",
  "email": "jane@company.com",
  "password": "securepassword123",
  "department": "Engineering",
  "designation": "Frontend Developer"
}
```

**Response** (`201 Created`):
```json
{
  "message": "User registered successfully",
  "id": 142,
  "email": "jane@company.com"
}
```

### 2. Login User
Authenticates a user and returns a JWT access token.

- **Method**: `POST`
- **Path**: `/auth/login`
- **Auth Required**: No

**Request Body**:
```json
{
  "email": "jane@company.com",
  "password": "securepassword123"
}
```

**Response** (`200 OK`):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "token_type": "bearer"
}
```

**Errors**:
- `401 Unauthorized`: Invalid email or password.

### 3. Get Current User (`/me`)
Retrieves the profile of the currently authenticated user.

- **Method**: `GET`
- **Path**: `/auth/me`
- **Auth Required**: Yes

**Response** (`200 OK`):
```json
{
  "id": 142,
  "name": "Jane Doe",
  "email": "jane@company.com",
  "role": "employee",
  "department": "Engineering",
  "designation": "Frontend Developer"
}
```

---

## 📚 Course Endpoints

### 1. List Courses
Fetches the catalog of available courses.

- **Method**: `GET`
- **Path**: `/courses/`
- **Auth Required**: Yes

**Response** (`200 OK`):
```json
[
  {
    "id": 1,
    "title": "Introduction to AI",
    "description": "Learn the basics of AI and ML.",
    "difficulty": "Beginner",
    "duration_minutes": 120
  }
]
```

---

## 🤖 AI Knowledge Base & RAG Endpoints

### 1. Query Knowledge Base
Submit a query to the enterprise knowledge base, processed via ChromaDB and Google Gemini.

- **Method**: `POST`
- **Path**: `/knowledge/query`
- **Auth Required**: Yes

**Request Body**:
```json
{
  "query": "What is our policy on remote work?"
}
```

**Response** (`200 OK`):
```json
{
  "answer": "According to the HR manual (2025), remote work is allowed up to 3 days a week...",
  "sources": [
    {
      "document": "HR_Policy_2025.pdf",
      "relevance_score": 0.94
    }
  ]
}
```

---

## 🛡️ Error Handling Conventions

The API consistently returns errors in the following JSON format:

```json
{
  "detail": "Human readable error message explaining what went wrong."
}
```

Standard Status Codes used:
- `400 Bad Request`: Validation failure or bad input.
- `401 Unauthorized`: Missing or invalid JWT.
- `403 Forbidden`: User lacks RBAC permissions (e.g., trying to access an Admin route).
- `404 Not Found`: Resource does not exist.
- `422 Unprocessable Entity`: Pydantic schema validation failure.
