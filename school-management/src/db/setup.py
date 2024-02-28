from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import date

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    cmnd = Column(String)
    birth_day = Column(Date)
    phone = Column(String)

    def __str__(self):
        return f"{self.name} - {self.address} - {self.cmnd} - {self.birth_day}"

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    cmnd = Column(String)
    birth_day = Column(Date)
    phone = Column(String)

    def __str__(self):
        return f"{self.name} - {self.address} - {self.cmnd} - {self.birth_day}"
    
    


def create_conections():
    Base.metadata.create_all(engine)
