# карта, построение маршрута, выдача путевых и опорных точек
class Navigator:

    map = None # собственно карта
    vertexes = [] # вершины
    edges = [] # ребра

    ways = [] # просмотренные вершины (для поиска пути)

    def __init__(self, db, mediator, mapId):
        self.db = db
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        if mapId:
            self.map = db.getMap(mapId)
            if self.map:
                self.vertexes = db.getVertexes(self.map['id'])
                self.edges = db.getEdges(self.map['id'])
        self.mediator.subscribe(self.TYPES['MAKE_ORDER'], self.makeOrder)

    # найти вершину по id
    def getVertex(self, id):
        result = [x for x in self.vertexes if x['id'] == id]
        return result[0] if len(result) else None

    # найти путь полета
    def findWays(self, start, finish):
        
        # пометить вершину пройденной
        print(start)
        
        edges = [x for x in self.edges if x['vertex1'] == start['id'] or x['vertex2'] == start['id']]
        for edge in edges:
            if edge['vertex1'] == finish['id'] or edge['vertex2'] == finish['id']: # если выход - ништяк
                for way in self.ways: # дописать выход в выходной путь
                    if (way[len(way) - 1]) == start['id']:
                        way.append(finish['id'])
                return True
            # взять все выходы из вершины, кроме уже пройденных
            for way in self.ways: # найти непомеченную вершину
                if (not len([x for x in way if x == edge['vertex1']])):
                    way.append(edge['vertex1'])
                    self.findWays([x for x in self.vertexes if x['id'] == edge['vertex1']][0], finish)
                if (not len([x for x in way if x == edge['vertex2']])):
                    way.append(edge['vertex2'])
                    self.findWays([x for x in self.vertexes if x['id'] == edge['vertex2']][0], finish)
            #...

        # иначе повторить для всех остальных выходов
        # если выходов больше одного - продублировать записи с путями

    # сделать полетное задание
    def makeOrder(self, options):
        start  = self.getVertex(options['start' ]) # точка старта маршрута
        finish = self.getVertex(options['finish']) # точка финиша маршрута
        if start and finish: 
            self.ways = [] # обнулить список путей
            self.ways.append([start['id']])
            if self.findWays(start, finish): # поиск путей
                print('Путь нашелся!!!', self.ways)
                #... полет
                #... разгрузка
                #backWay = self.findWay(finish, start, self.edges) # путь обратно
                #... полет обратно
                return True
        return False
