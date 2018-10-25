class UserManager:

    def __init__(self, db):
        self.db = db

    def login(self, login):
        user = self.db.getUserByLogin(login)
        return user