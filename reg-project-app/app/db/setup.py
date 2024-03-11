from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Table, Float
from datetime import date
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define association table for Group and Account
group_account_association = Table('group_account_association', Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('account_id', Integer, ForeignKey('account.id'))
)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    cmnd = Column(String)
    birth_day = Column(Date)

    def __str__(self):
        return f"{self.name} - {self.address} - {self.cmnd} - {self.birth_day}"

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    cmnd = Column(String)
    birth_day = Column(Date)

    def __str__(self):
        return f"{self.name} - {self.address} - {self.cmnd} - {self.birth_day}"

project_account_association = Table('project_account_association', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('account_id', Integer, ForeignKey('account.id'))
)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    done = Column(Boolean)
    deadline = Column(Date)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    project = relationship("Project", back_populates="tasks")
    account_id = Column(Integer, ForeignKey('account.id'), nullable=True)
    account = relationship("Account", back_populates="tasks")
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    group = relationship("Group", back_populates="tasks")

    def __str__(self):
        return f"{self.name} - {self.description} - {self.deadline} - {self.project_id} - {self.account_id}"

# Modify Project class to include a relationship with Account
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    accounts = relationship("Account", secondary=project_account_association, back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    groups = relationship("Group", back_populates="project")

    def __str__(self):
        return f"{self.name} - {self.description} - {self.start_date} - {self.end_date}"



# Define Group class with relationship to Account
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    accounts = relationship("Account", back_populates="group")
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    project = relationship("Project", back_populates="groups")
    tasks = relationship("Task", back_populates="group")

    def __str__(self):
        return f"{self.name}"
    

# Modify Account class to include a relationship with Project
class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    fullname = Column(String)
    email = Column(String)
    phone = Column(String)
    birthday = Column(Date)
    password = Column(String)
    role = Column(String, default='user')
    projects = relationship("Project", secondary=project_account_association, back_populates="accounts")
    tasks = relationship("Task", back_populates="account")
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=True)
    group = relationship("Group", cascade="all,delete", back_populates="accounts" )
    grade_id = Column(Integer, ForeignKey('grades.id'), nullable=True)
    grade = relationship("Grade", back_populates="accounts", cascade="all,delete")
    def __str__(self):
        return f"{self.username} - {self.fullname} - {self.email} - {self.phone} - {self.birthday} - {self.role}"
class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mark = Column(Float)
    date = Column(Date)
    accounts = relationship("Account", back_populates="grade")

    def __str__(self):
        return f"{self.student_id} - {self.subject} - {self.mark} - {self.date}"

def create_connections():
    Base.metadata.create_all(engine)

