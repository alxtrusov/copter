# медиатор
class Mediator:
    TYPES = {} # типы событий
    events = {} # списки событий

    def __init__(self, events):
        self.TYPES = events
        for key in self.TYPES.keys():
            self.events.update({ self.TYPES[key]: [] })

    def __del__(self):
        self.events.clear()

    def getTypes(self):
        return self.TYPES.keys()

    # получить название события
    #def get(self, name):
        #return self.TYPES.get(name)

    # дернуть функции, чтобы исполнялись
    def call(self, name, data = None):
        if (name):
            cbs = self.events.get(name)
            if cbs:
                for cb in cbs:
                    cb(data)

    # подписаться на событие
    def subscribe(self, name, func):
        if name and func:
            self.events.get(name).append(func)