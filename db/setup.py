from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Class to denote users 
class Users(Base):
    
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    salt = Column(String(100), nullable=False)
    date_created = Column(String(10), nullable=False)

    images = relationship("Images", backref = "Users")
    likes = relationship("Likes", backref = "Users")

class Images(Base):

    __tablename__ = 'Images'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    caption = Column(String(100), nullable=False)
    image_path = Column(String(50), nullable=False)
    date_created = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))
    
    likes = relationship("Likes", backref = "Images")
    
    
class Likes(Base):

    __tablename__ = "Likes"
    
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("Images.id"))
    user_id = Column(Integer, ForeignKey("Users.id"))
    date_liked = Column(String(10), nullable=False)  
    

# Connect to and create the movie table
engine = create_engine("sqlite:///Images.db")
Base.metadata.create_all(engine)

