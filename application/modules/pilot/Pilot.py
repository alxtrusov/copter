# автопилот
class Pilot:

    def __init__(self, db, mediator):
        self.db = db
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
