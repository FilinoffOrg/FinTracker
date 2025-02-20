from pydantic import BaseModel, Field

class UserLoginSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserCreateSchema(UserLoginSchema):
    pass

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

