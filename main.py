# Main FastAPI app

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session
import uvicorn

import crud, models, schemas
from database import SessionLocal, engine

from fastapi.middleware.wsgi import WSGIMiddleware
from flask_web.main import app as flask_app

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# craete fastapi (app) instance
fapp = FastAPI()



# need to have an independent database session/connection
# this function lets us to use the same connection throughout request lifecycle
# to accomplish the task above we will use this function as dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    # even if we catch an error the connection is gonna be closed
    finally:
        db.close()

# Create New User
@fapp.post("/users/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.get_user_by_email(db, user_email=user.email)
    if len(user.password) < 7:
        raise HTTPException(status_code=404, detail="Pasword too short")
    if new_user:
        raise HTTPException(status_code=400, detail="Email is already taken by another user. Use another.")
    return crud.create_user(db=db, user=user)


# getting a user with a specific email which is unique
@fapp.get("/users/{email}", response_model=schemas.User)
def get_certain_user(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User with this Email doesn't exists")
    return user

# Update User by Email
@fapp.put("/users/update/{email}")
def get_update_user(email, full_name, password, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User with this Email doesn't exists")
    check = crud.update_user(db, email, full_name, password)
    if check == 'Password too short':
        raise HTTPException(status_code=404, detail="Pasword too short")
    return crud.get_user_by_email(db, email)

# Delete user by Email
@fapp.delete("/users/delete/{email}")
def user_delete(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User with this Email doesn't exists")
    crud.delete_user(db, email)
    return Response('User was deleted!')

# creating a new post
@fapp.post("/posts/", response_model=schemas.Post)
def create_post(user_id:int, post: schemas.PostCreate, db: Session=Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User with this ID doesn't exists, NOTE DON'T CREATED!")
    return crud.create_post(user_id=user_id, db=db, post=post)


# getting a specific user's posts
@fapp.get("/user/posts/{user_id}", response_model=list[schemas.Post])
def get_user_posts(user_id, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User with this ID doesn't exists, NOTE DON'T CREATED!")
    post = crud.get_user_posts(db, user_id)
    if not post:
        raise HTTPException(status_code=200, detail="This user haven't notes")
    return post

# getting a certain Post by its id
@fapp.get("/user/{post_id}/", response_model=schemas.Post)
def get_post_by_id(post_id:int, db: Session = Depends(get_db)):
    post = crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="This note doesn't exist")
    return post

# Update Uset's note
@fapp.put("/user/update-post/{post_id}")
def update_post(post_id: int, title: str, content: str, db: Session = Depends(get_db)):
    post = crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Note with this ID doesn't exists")
    crud.update_post(db, post_id, title, content)
    return crud.get_post_by_id(db, post_id)

# Delete user's note
@fapp.delete("/user/delete_post/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Note with this ID doesn't exists")
    crud.delete_post(db, post_id)
    return Response('Note was deleted!')

fapp.mount("/", WSGIMiddleware(flask_app))

if __name__ == '__main__':
    uvicorn.run(fapp, host='127.0.0.1', port=8000)