from pydantic import BaseModel, Field

class userArgument(BaseModel):
    email : str = Field(..., title="sigin id", regex="[^@]+@[^@]+\.[^@]+")
    password : str = Field(..., title="password")