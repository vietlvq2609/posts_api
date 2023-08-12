from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from datetime import datetime


# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Image(BaseModel):
    url: str

# Posts
class BasePost(BaseModel):
    title: str
    short_desc: str | None = None
    desc: str
    images: list[Image] = []
    class Config:
        schema_example = {
            "title": "Chào mừng 20-11",
            "short_desc": "Các sự kiện trong dịp ngày Nhà giáo Việt Nam",
            "desc": "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur",
            "create_at":  "2023-06-01T10:30:00Z"
        }

class PostIn(BasePost):
    pass

class PostOut(BasePost):
    id: int
    likes: str | None = None
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

# Users
class BaseUser(BaseModel):
    username: str
    email: EmailStr

class UserIn(BaseUser):
    password: str
    avatar: UploadFile | None = None
class UserAuthenticate(BaseUser):
    id: int

class UserOut(BaseUser):
    id: int
    posts: list[PostOut] = []
    avatar: str

    class Config:
        orm_mode = True

# Comments
class BaseComment(BaseModel):
    content = str

class CommentIn(BaseComment):
    pass

class CommentOut(BaseComment):
    id = int
    user_id = int