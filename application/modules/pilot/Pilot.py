import requests
import json
from .DroneKit import DroneKit

# автопилот
class Pilot:

    point = None # текущая точка нахождения
    droneKit = None # плагин для управления коптером

    def __init__(self, db, mediator):
        self.db = db
        self.mediator = mediator
        self.TYPES = mediator.getTypes()

        self.droneKit = DroneKit()

        # подписки на события
        self.mediator.subscribe(self.TYPES['TERMINATE_PATHWAY'], self.terminatePathway)
        self.mediator.subscribe(self.TYPES['FIRST_POINT'], self.firstPoint)
        self.mediator.subscribe(self.TYPES['NEXT_POINT'], self.nextPoint)
        self.mediator.subscribe(self.TYPES['LAST_POINT'], self.lastPoint)
        self.mediator.subscribe(self.TYPES['SIMPLE_ARM'], self.simpleArm)

    '''
    ОБРАБОТЧИКИ СОБЫТИЙ
    '''
    # прекратить полет
    def terminatePathway(self, options):
        #...
        print('stop execute pathway in pilot')
        return True

    # получил первую точку полетного маршрута
    def firstPoint(self, options):
        vertex = options['vertex'] if 'vertex' in options.keys() else None
        if (vertex):
            print('first point', vertex)
            # взлететь
            #...
            self.mediator.call(self.TYPES['GET_NEXT_POINT']) # запросить следующую точку
            return True
        return False

    # получил следующую точку полетного маршрута
    def nextPoint(self, options):
        nextVertex = options['next'] if 'next' in options.keys() else None # следующая точка маршрута
        prevVertex = options['prev'] if 'prev' in options.keys() else None # предыдущая точка маршрута
        if nextVertex:
            print('Go To point', prevVertex, nextVertex)
            # лететь в точку nextVertex
            #...
            self.mediator.call(self.TYPES['GET_NEXT_POINT']) # запросить следующую точку маршрута
            return True
        print('All going wrong! Next point is empty! Terminate pathway')
        self.mediator.call(self.TYPES['TERMINATE_PATHWAY'])
        return False
        
    # получил последнюю точку полетного маршрута
    def lastPoint(self, options):
        vertex = options['vertex'] if 'vertex' in options.keys() else None
        task   = options['task'  ] if 'task'   in options.keys() else None # приказ на выполнение задания
        if (vertex and task): # выполнить полетное задание
            print('last point', vertex, task)
            # выполнить полетное задание
            #...
            # завершить маршрут и начать выполнять следующий маршрут
            print('!!!START_NEXT_PATHWAY!!!')
            self.mediator.call(self.TYPES['TERMINATE_PATHWAY'])
            #self.mediator.call(self.TYPES['START_NEXT_PATHWAY'])
            return True
        return False

    def simpleArm(self, options):
        try: 
            print('send to: http://46.61.183.14:3000/wind')
            r = requests.get('http://46.61.183.14:3000/wind', timeout=1)
            if r.status_code == 200:
                print(json.loads(r.text))
        except requests.exceptions.RequestException as e:
            print(e)
        self.droneKit.simpleArm()
        return True