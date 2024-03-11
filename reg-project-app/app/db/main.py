'''
    Importing the database object from the models file
    and creating a function to initialize the database
'''
# DAO class
from app.db.dao.interface_dao import InterfaceDao
from app.db.dao.account_dao import AccountDao 
from app.db.dao.student_dao import StudentDao
from app.db.dao.teacher_dao import TeacherDao
from app.db.dao.project_dao import ProjectDao
from app.db.dao.group_dao import GroupDao
from app.db.dao.task_dao import TaskDao
from app.db.dao.grade_dao import GradeDao

# Database class
from app.db.setup import Account, Student, Teacher, Project, Task, Group, Grade