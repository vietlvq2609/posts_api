from sqlalchemy.orm import Session
from fastapi import UploadFile
from pydantic import EmailStr
from datetime import datetime
from . import models, schemas, utils
import os

SERVER_URL = "http://127.0.0.1:8000"


# USER CONTROLLER
def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user_data = user.__dict__
    user_data["posts"] = (
        db.query(models.Post).filter(models.Post.created_by == user.id).all()
    )
    return user_data


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    user_data = {}
    if user:
        user_data = user.__dict__
        user_data["posts"] = db.query(models.Post).filter(models.Post.created_by == user.id).all()
    return user_data


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    users_data = []
    for user in users:
        user_data = user.__dict__
        user_data["posts"] = (
            db.query(models.Post).filter(models.Post.created_by == user.id).all()
        )
        users_data.append(user_data)
    return users_data


async def create_user(
    db: Session, username: str, email: EmailStr, password: str, avatar: UploadFile
):
    directory = "app/uploads"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_name = avatar.filename.replace(" ", "-").split(".")[0]
    file_path = os.path.join(directory, file_name)
    with open(file_path, "wb") as buffer:
        file_content = await avatar.read()
        buffer.write(file_content)

    db_user = models.User(
        username=username,
        email=email,
        hashed_password=utils.get_password_hash(password),
        avatar=f"{SERVER_URL}/files/{file_name}",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def change_password(db: Session, user_id: int, new_password: str):
    fake_hased_password = new_password + "notreallyhased"
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.hashed_password = fake_hased_password
    db.commit()
    db.refresh(db_user)
    return db_user


def update_profile(db: Session, user: schemas.UserIn):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    db_user.email = user.email
    db_user.username = user.username
    db.commit()
    db.refresh(db_user)
    return db_user


# PRODUCT CONTROLLER
def get_posts(db: Session, skip: int, limit: int):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def create_post(
    db: Session, post: schemas.PostIn, current_user: schemas.UserAuthenticate
):
    db_post = models.Post(
        title=post.title,
        short_desc=post.short_desc,
        desc=post.desc,
        created_at=datetime.now(),
        created_by=current_user,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post: schemas.PostIn, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db_post.title = post.title
    db_post.short_desc = post.short_desc
    db_post.desc = post.desc
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return {"message": "Deleted post with id " + str(post_id)}
