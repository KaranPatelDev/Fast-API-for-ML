from pydantic import BaseModel, Field, StrictInt
from typing import Optional

class Employee(BaseModel):
    id: int = Field(..., gt=0, title="Employee ID")
    name: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z ]+$")
    department: str = Field(..., min_length=2, max_length=50)
    age: Optional[StrictInt] = Field(default=None, ge=21)