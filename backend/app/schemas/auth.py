from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: str
    designation: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdatePasswordRequest(BaseModel):
    email: EmailStr
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    

    