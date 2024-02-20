from app.db.dao.interface_dao import InterfaceDao
from app.db.setup import session, Account

class AccountDao(InterfaceDao):
    def __init__(self, session = session):
        self.session = session

    def add(self, account):
        self.session.add(account)
        self.session.commit()

    def update(self, account):
        self.session.merge(account)
        self.session.commit()

    def delete(self, account):
        self.session.delete(account)
        self.session.commit()

    def get_all(self):
        return self.session.query(Account).all()

    def get_by_id(self, id):
        return self.session.query(Account).filter(Account.id == id).first()