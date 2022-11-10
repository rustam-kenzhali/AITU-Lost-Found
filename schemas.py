from pydantic import BaseModel, validator


class PostBase(BaseModel):
    title: str
    content: str
    lostfound: str
    image: str
    author: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    post_id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str

    @validator('email')
    def check_email(cls, v):
        if '@astanait.edu.kz' in v:
            return v
        else:
            raise ValueError("Use only university corporate mail")


class UserCreate(UserBase):
    password: str
    full_name: str
    group: str
    phone_number: str



# will be used when reading data, when returning it from the API.
class User(UserBase):
    id: int
    posts: list[Post] = []

    class Config:
        orm_mode = True

