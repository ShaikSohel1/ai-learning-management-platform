from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    category: str = Field(..., min_length=2, max_length=100)
    duration: int = Field(..., gt=0)
    difficulty: str = Field(..., min_length=3, max_length=50)

class CourseUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    category: str = Field(..., min_length=2, max_length=100)
    duration: int = Field(..., gt=0)
    difficulty: str = Field(..., min_length=3, max_length=50)

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    duration: int
    difficulty: str
    created_by: int

    model_config = ConfigDict(from_attributes=True)