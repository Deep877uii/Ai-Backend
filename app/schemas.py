from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, conint
from typing import Annotated

class postbase(BaseModel):
    title: str
    content: str
    publisher: bool = True
    rating: Optional[int] = None


class create_post(postbase):
    pass

class create_user(BaseModel):
    email: EmailStr
    password: str


class response_user(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    

    class Config:
        from_attributes = True

class user_login(BaseModel):
    email: EmailStr
    password: str


class response_post(postbase):
    id: int
    created_at: datetime
    owner_id : int
    owner : response_user

    class Config:
        from_attributes = True

class response_post_vote(BaseModel):
    Post: response_post
    votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None



class Vote(BaseModel):
    post_id: int
    direction: Annotated[int, Field(ge=0, le=1)]