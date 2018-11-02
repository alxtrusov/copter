# авторизация, разграничение прав доступа
class User:
    def __init__(self, db, mediator):
        self.db = db
        self.mediator = mediator