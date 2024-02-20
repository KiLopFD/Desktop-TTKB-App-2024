from app.db.dao.interface_dao import InterfaceDao
from app.db.setup import session, Teacher

class TeacherDao(InterfaceDao):
    def __init__(self, session = session):
        self.session = session

    def add(self, teacher):
        self.session.add(teacher)
        self.session.commit()

    def update(self, teacher):
        self.session.merge(teacher)
        self.session.commit()

    def delete(self, teacher):
        self.session.delete(teacher)
        self.session.commit()

    def get_all(self):
        return self.session.query(Teacher).all()

    def get_by_id(self, id):
        return self.session.query(Teacher).filter(Teacher.id == id).first()