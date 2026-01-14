from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    user_posts: Mapped[List["Post"]] = relationship(back_populates="user")
    user_interactions: Mapped[List["Interactions"]] = relationship(back_populates="user")
    user_messages: Mapped[List["Messages"]] = relationship(back_populates="user")
    user_follows: Mapped[List["Follows"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_text: Mapped[str] = mapped_column(String(300), nullable=True)
    img_link: Mapped[str] = mapped_column(String(200), nullable=False)
    post_link: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="user_posts")
    post_id: Mapped[List["Interactions"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_text": self.post_text,
            "img_link": self.img_link,
            "post_link": self.post_link
        }
    
class Interactions(db.Model):
    __tablename_ = "interactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    like: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    comment: Mapped[str] = mapped_column(String(200), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] =mapped_column(ForeignKey("post.id"))

    user: Mapped["User"] = relationship(back_populates="user_interactions")
    post: Mapped["Post"] = relationship(back_populates="post_id")

    def serialize(self):
        return {
            "id":self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "like": self.like,
            "comment": self.comment
        }

class Messages(db.Model):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(200), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="user_messages")

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "sender_id": self.sender_id,
            "reciever_id": self.receiver_id
        }
    
class Follows(db.Model):
    __tablename__ = "follows"
    id: Mapped[int] = mapped_column(primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="user_follows")


    def serialize(self):
        return {
            "id": self.id,
            "followed_id": self.followed_id,
            "follower_id": self.follower_id
        }