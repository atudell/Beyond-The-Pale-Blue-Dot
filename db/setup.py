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

class Images(Base):

    __tablename__ = 'Images'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    caption = Column(String(100), nullable=False)
    image_path = Column(String(50), nullable=False)
    date_created = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))
       

# Connect to and create the movie table
engine = create_engine("mysql+pymysql://{username}:{password}@{host}/{database_name}")
Base.metadata.create_all(engine)

