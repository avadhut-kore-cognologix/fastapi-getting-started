from pydantic import BaseModel
from db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

like_posts = Table (
    "like_posts",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 1:M mapping : one user can own multiple notes
    notes = relationship("Note", back_populates="owner")
    # 1:M mapping : one user can author multiple posts
    posts = relationship("Post", back_populates="author")

    posts_liked = relationship("Post", secondary=like_posts, back_populates="liked_by_users")

class ResetPassword(Base):
    __tablename__ = "reset_passwords"

    email = Column(String, primary_key=True)
    code = Column(String)
    
    

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # 1:1 mapping : one note owned by one user
    owner = relationship("User", back_populates="notes")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    # 1:1 mapping : one post authored by one user
    author = relationship("User", back_populates="posts")

    # M:M mapping : one user can like multiple posts
    liked_by_users = relationship("User", secondary=like_posts, back_populates="posts_liked")


class Item(BaseModel):
    name: str
    description: str or None = None # type: ignore
    price: float
    tax: float or None = None # type: ignore
    tags: set[str] = set

class BaseUser(BaseModel):
    name: str
    email: str
    username: str

class UserIn(BaseUser):
    password: str

class UserOut(BaseUser):
    pass
