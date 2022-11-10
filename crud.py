# CReateUpdateDelete utils (CRUD)
# reusable functions to interact with the data in the database.
from fastapi import Query
from sqlalchemy.orm import Session
import models, schemas
from werkzeug.security import generate_password_hash

# getting a user by email from a query to Users table using SQLAlchemy model User
def get_user_by_email(db: Session, user_email: str) -> Session.query:
    return db.query(models.User).filter(models.User.email == user_email).first()

# getting a user by id
def get_user_by_id(db: Session, user_id: str) -> Session.query:
    return db.query(models.User).filter(models.User.id == user_id).first()

# creating a user from instance of UserCreate
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    new_user = models.User(email=user.email,
                           password=generate_password_hash(user.password, method='sha256'),
                           full_name=user.full_name,
                           group=user.group,
                           phone_number=user.phone_number
                           )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update username and Password
def update_user(db: Session, user_email: str, full_name:str, password:str) -> Session.query:
    if len(password) < 7:
        return 'Password too short'
    user = get_user_by_email(db, user_email)
    user.full_name = full_name
    user.password = generate_password_hash(password, method='sha256')



    db.commit()
    db.refresh(user)

# Delete user by Email
def delete_user(db: Session, email):
    user = get_user_by_email(db, email)

    posts = get_user_posts(db, user.id)
    for post in posts:
        db.delete(post)
        db.commit()

    db.delete(user)
    db.commit()


# creating a note from instance of NoteCreate
def create_post(db: Session, post: schemas.PostCreate, user_id) -> models.Post:
    new_post = models.Post(title=post.title,
                           content=post.content,
                           lostfound=post.lostfound,
                           image=post.image,
                           author=post.author,
                            user_id=user_id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# getting a post by a post_id
def get_post_by_id(db: Session, post_id: int) -> Session.query:
    return db.query(models.Post).filter(models.Post.post_id == post_id).first()

# getting a user posts
def get_user_posts(db: Session, user_id: int) -> Session.query:
    return db.query(models.Post).filter(models.Post.user_id == user_id).all()


# UPDATE NOTE
def update_post(db: Session, post_id: int, title: str, content: str) -> Session.query:
    post = get_post_by_id(db, post_id)
    post.title = title
    post.content = content

    db.commit()
    db.refresh(post)


def delete_post(db:Session, post_id):
    post = get_post_by_id(db, post_id)
    db.delete(post)
    db.commit()
