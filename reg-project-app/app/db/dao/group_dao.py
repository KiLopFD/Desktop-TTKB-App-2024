from app.db.dao.interface_dao import InterfaceDao
from app.db.setup import session, Group

class GroupDao(InterfaceDao):
    def __init__(self, session = session):
        self.session = session
    
    def get(self, id: int) -> Group:
        return self.session.query(Group).get(id)

    def add(self, group):
        self.session.add(group)
        self.session.commit()

    def update(self, group):
        self.session.merge(group)
        self.session.commit()

    def delete(self, group):
        self.session.delete(group)
        self.session.commit()

    def get_all(self):
        return self.session.query(Group).all()

    def get_by_id(self, id):
        return self.session.query(Group).filter(Group.id == id).first()
    
    def delete_all(self):
        self.session.query(Group).delete()
        self.session.commit()