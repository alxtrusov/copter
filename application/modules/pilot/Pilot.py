# автопилот
class Pilot:

    def __init__(self, db, mediator):
        self.db = db
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        # подписки на события
        self.mediator.subscribe(self.TYPES['TERMINATE_PATHWAY'], self.terminatePathway)
        self.mediator.subscribe(self.TYPES['NEXT_POINT'], self.nextPoint)

    # прекратить полет
    def terminatePathway(self, options):
        #...
        print('stop execute pathway in pilot')
        return True

    # получить следующую точку полета
    def nextPoint(self, options):
        vertex = options['next']
        print(vertex)
        
