from app.db.dao.interface_dao import InterfaceDao
from app.db.setup import session, Project


class ProjectDao(InterfaceDao):
    def __init__(self, session = session):
        self.session = session

    def add(self, project):
        self.session.add(project)
        self.session.commit()

    def update(self, project):
        self.session.merge(project)
        self.session.commit()

    def delete(self, project):
        self.session.delete(project)
        self.session.commit()

    def get_all(self):
        return self.session.query(Project).all()

    def get_by_id(self, id):
        return self.session.query(Project).filter(Project.id == id).first()