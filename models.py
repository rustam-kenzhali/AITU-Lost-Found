from sqlalchemy import  Integer, String, Column, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'post'
    post_id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    content = Column(String(10000))
    lostfound = Column(String(50))
    image = Column(String(1000))
    author = Column(String(150))
    user_id = Column(Integer, ForeignKey('user.id'))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(150))
    full_name = Column(String(150))
    group = Column(String(100))
    phone_number = Column(String(15))


    posts = relationship('Post')


