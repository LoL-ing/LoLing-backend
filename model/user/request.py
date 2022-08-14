from pydantic import BaseModel, Field

class UserRegisterArgument(BaseModel):
    email : str = Field(..., title="sigin id", regex="[^@]+@[^@]+\.[^@]+")
    password : str = Field(..., title="password")
    password_confirm : str = Field(..., title="password")