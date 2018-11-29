# карта, построение маршрута, выдача путевых и опорных точек
class Navigator:

    SETTINGS = None
    map = None # собственно карта
    vertexes = [] # вершины
    edges    = [] # ребра
    currentPath = None # текущий путь
    currentPoint = 0 # текущая точка пути

    def __init__(self, db, mediator, mapId, settings):
        self.db = db
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        self.SETTINGS = settings
        if mapId:
            self.map = db.getMap(mapId)
            if self.map:
                self.vertexes = db.getVertexes(self.map['id'])
                self.edges = db.getEdges(self.map['id'])
        # если имеется непройденный маршрут
        launchPath = self.db.getLaunchPathway()
        if launchPath:
            self.setCurrentPath(launchPath)
        # подписки на события
        self.mediator.subscribe(self.TYPES['MAKE_PATHWAY'      ], self.makePathway     )
        self.mediator.subscribe(self.TYPES['START_NEXT_PATHWAY'], self.startNextPathway)
        self.mediator.subscribe(self.TYPES['TERMINATE_PATHWAY' ], self.terminatePathway)
        self.mediator.subscribe(self.TYPES['GET_NEXT_POINT'    ], self.getNextPoint    )

    '''
    СЛУЖЕБНЫЕ МЕТОДЫ
    '''
    # найти вершину по id
    def getVertex(self, id):
        result = [x for x in self.vertexes if x['id'] == id]
        return result[0] if len(result) else None

    # вернуть список выходов из вершины по id
    def getNextVertexes(self, id):
        result = []
        edges = [x for x in self.edges if x['vertex1'] == id or x['vertex2'] == id]
        for edge in edges: 
            if edge['vertex1'] != id: # не очень красиво, зато безопасно, потому что исключается возможность ребра-петли
                result.append(edge['vertex1'])
            if edge['vertex2'] != id:
                result.append(edge['vertex2'])
        return result if len(result) else None

    # рекурсивный алгоритм поиска пути маршрута по графу
    def findWay(self, startId, finishId, way):
        if startId == finishId: # если нашли выход
            way.append(finishId)
            return way
        # выхода пока нет, идти дальше по ребрам
        ways = self.getNextVertexes(startId) # список выходов из вершины
        if (ways):
            # взять непройденные выходы
            ways = list(set(ways) - set(way)) # вычитание, по сути, одного массива из другого
            if len(ways): # список непройденных вершин-выходов ещё есть
                for w in ways:
                    newWay = self.findWay(w, finishId, way + [startId]) # находим новый путь, добавляя к старому текущую вершину
                    if (newWay): 
                        return newWay
        return None

    # очистить текущий путь
    def clearCurrentPath(self):
        self.currentPath = None
        self.currentPoint = 0

    # выставить новый текущий путь
    def setCurrentPath(self, way):
        self.currentPath = way
        self.currentPoint = 0

    # переводит строку с массивом в массив вершин
    def strPathToArray(self, path):
        path = path.replace('[', '').replace(']', '')
        path = [int(s) for s in path.split(', ')]
        return path

    '''
    ОБРАБОТЧИКИ СОБЫТИЙ
    '''
    # сделать полетное задание
    def makePathway(self, options):
        start  = self.getVertex(options['start' ]) # точка старта маршрута
        finish = self.getVertex(options['finish']) # точка финиша маршрута
        priority = options['priority']
        if start and finish and priority:
            way = self.findWay(start['id'], finish['id'], [])
            if way:
                TASK     = self.SETTINGS['TASK'    ]
                PRIORITY = self.SETTINGS['PRIORITY']
                if priority == PRIORITY['URGENT']: # супер-важное задание
                    self.db.setPathway(self.map['id'], str(way), priority, TASK['FLY']) # полет с зависанием
                else: # все остальные приоритеты
                    self.db.setPathway(self.map['id'], str(way), priority, TASK['DELIVERY']) # полет с разгрузкой
                    way.reverse() # перевернуть массив
                    self.db.setPathway(self.map['id'], str(way), priority, TASK['LANDING']) # полет с посадкой
                self.mediator.call(self.TYPES['NEW_PATHWAY'])
                return True
            else:
                print('Pathway is empty')
        return False

    # стартовать последовательное выполнение маршрутов
    def startNextPathway(self, options):
        id = options['id'] if 'id' in options.keys() else None
        if id: # выполнить один маршрут
            way = self.db.getPathway(id)
            if way: 
                way['path'] = self.strPathToArray(way['path']) # перевести строковый путь в массив вершин
                self.terminatePathway() # прекратить выполнение маршрута
                self.setCurrentPath(way) # выставить текущий маршрут
                self.db.updatePathwayStatus(self.currentPath['id'], 'launch')
                self.getNextPoint() # запустить пролет по маршруту
        else: # выполнить маршруты по их приоритетам
            ways = self.db.getPathways(self.map['id'])
            for way in ways:
                way['path'] = self.strPathToArray(way['path']) # перевести строковый путь в массив вершин
                # TODO ДОПИСАТЬ!!!
                #...
        return True

    # прекратить выполнение маршрута (любого)
    def terminatePathway(self, options = None):
        if self.currentPath: # погасить текущий путь в БД
            self.db.closePathway(self.currentPath['id'])
        self.clearCurrentPath()
        return True

    # получить следующую точку маршрута
    def getNextPoint(self, options = None):
        if self.currentPath:
            if self.currentPoint == 0: # первая точка маршрута
                vertex = self.getVertex(self.currentPath['path'][self.currentPoint])
                self.currentPoint += 1
                self.mediator.call(self.TYPES['FIRST_POINT'], { 'vertex': vertex })
                return True
            # остальные точки маршрута
            if (self.currentPoint < len(self.currentPath['path']) - 1):
                nextVertex = self.getVertex(self.currentPath['path'][self.currentPoint])
                prevVertex = self.getVertex(self.currentPath['path'][self.currentPoint - 1])
                self.currentPoint += 1
                self.mediator.call(self.TYPES['NEXT_POINT'], { 'next': nextVertex, 'prev': prevVertex })
                return True
            # последняя точка маршрута
            if self.currentPath:
                vertex = self.getVertex(self.currentPath['path'][self.currentPoint])
                self.mediator.call(self.TYPES['LAST_POINT'], { 'vertex': vertex, 'task': self.currentPath['task'] })
                return True
        return self.terminatePathway()
            