from sqlalchemy import Column, Integer, String, Text, DateTime , ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__="blogs"
    id=Column(Integer,primary_key=True,index=True)  
    title=Column(String)
    body=Column(Text)

    user_id=Column(Integer,ForeignKey('users.id'))

    created_by=relationship("AppUser",back_populates='blogs')

class AppUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs=relationship("Blog",back_populates='created_by')