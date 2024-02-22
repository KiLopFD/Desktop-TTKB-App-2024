'''
    Importing the database object from the models file
    and creating a function to initialize the database
'''
# DAO class
from app.db.dao.interface_dao import InterfaceDao
from app.db.dao.account_dao import AccountDao 
from app.db.dao.student_dao import StudentDao
from app.db.dao.teacher_dao import TeacherDao

# Database class
from app.db.setup import Account, Student, Teacher