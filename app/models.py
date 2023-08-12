from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from .database import Base

# USER MODEL
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    avatar = Column(String)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

# POST MODEL
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    short_desc = Column(String, default="")
    desc = Column(Text)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('users.id'))
    likes = Column(String)

    user = relationship('User', back_populates="posts")
    images = relationship("Image", back_populates="post")
    comments = relationship("Comment", back_populates="post")

# COMMENT MODEL
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    user = relationship('User', back_populates="comments")
    post = relationship('Post', back_populates="comments")

# IMAGE MODEL
class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))

    post = relationship("Post", back_populates="images")
