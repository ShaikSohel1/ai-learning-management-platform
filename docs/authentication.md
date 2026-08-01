# Authentication & JWT Security Specification

This document details the user authentication workflows, JWT token issuance, password reset mechanics, and Role-Based Access Control (RBAC).

---

## 🔐 JWT Authentication Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant React as React Client
    participant API as FastAPI Backend
    participant DB as Supabase PostgreSQL

    User->>React: Enter Email & Password
    React->>API: POST /auth/login
    API->>DB: Query user by email
    DB-->>API: Return hashed_password
    API->>API: Verify Bcrypt password hash
    API->>API: Generate Signed JWT Token (HS256)
    API-->>React: 200 OK (access_token, token_type, user_dto)
    React->>React: Store token in LocalStorage / Auth Header
    
    rect rgb(240, 255, 240)
        note over React,API: Authenticated Request Execution
        React->>API: GET /courses (Authorization: Bearer <token>)
        API->>API: Verify JWT signature & expiration
        API-->>React: 200 OK (Protected Data)
    end
```

---

## 🔑 Password Reset Protocol

1. **Request Reset**: User posts email to `POST /auth/forgot-password`.
2. **Token Issue**: Backend creates a 64-character random hex token in `password_reset_tokens` table with `expires_at = NOW() + 15 mins`.
3. **Email Delivery**: Token reset URL is delivered via Resend Email API (`/reset-password?token=...`).
4. **Token Consumption**: User posts new password and token to `POST /auth/reset-password`. Token is marked `used = true`.
