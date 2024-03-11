from app.db.dao.interface_dao import InterfaceDao
from app.db.setup import session, Task

class TaskDao(InterfaceDao):
    def __init__(self, session = session):
        self.session = session

    def add(self, task):
        self.session.add(task)
        self.session.commit()

    def update(self, task):
        self.session.merge(task)
        self.session.commit()

    def delete(self, task):
        self.session.delete(task)
        self.session.commit()

    def get_all(self):
        return self.session.query(Task).all()

    def get_by_id(self, id):
        return self.session.query(Task).filter(Task.id == id).first()
    
    def delete_all(self) -> bool:
        try:
            self.session.query(Task).delete()
            self.session.commit()
            return True
        except:
            return False