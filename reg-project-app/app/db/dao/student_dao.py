from app.db.dao.interface_dao import InterfaceDao
from app.db.setup import session, Student

class StudentDao(InterfaceDao):
    def __init__(self, session = session):
        self.session = session

    def add(self, student):
        self.session.add(student)
        self.session.commit()

    def update(self, student):
        self.session.merge(student)
        self.session.commit()

    def delete(self, student):
        self.session.delete(student)
        self.session.commit()

    def get_all(self) -> list[Student]:
        return self.session.query(Student).all()

    def get_by_id(self, id):
        return self.session.query(Student).filter(Student.id == id).first()