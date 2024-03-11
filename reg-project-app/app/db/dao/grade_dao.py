from app.db.dao.interface_dao import InterfaceDao
from app.db.setup import session, Grade

class GradeDao(InterfaceDao):
    def __init__(self, session = session):
        self.session = session

    def add(self, grade):
        self.session.add(grade)
        self.session.commit()

    def update(self, grade):
        self.session.merge(grade)
        self.session.commit()

    def delete(self, grade):
        self.session.delete(grade)
        self.session.commit()

    def get_all(self):
        return self.session.query(Grade).all()
    
    def get_by_id(self, id):
        return self.session.query(Grade).filter(Grade.id == id).first()
    
    def delete_all(self):
        self.session.query(Grade).delete()
        self.session.commit()
        