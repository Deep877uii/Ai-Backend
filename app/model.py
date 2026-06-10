from email.policy import default
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, Integer, String,Boolean ,ForeignKey   
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP 

class Post(Base):
    __tablename__ = "Post"
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    publisher = Column(Boolean,server_default='True',nullable=False)
    rating = Column(Integer,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("user.id", ondelete="CASCADE"),nullable=False)
    
    owner = relationship("user")

class user(Base):
    __tablename__ ="user"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class vote(Base):
    __tablename__ ="vote"
    post_id = Column(Integer,ForeignKey("Post.id", ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),primary_key=True)