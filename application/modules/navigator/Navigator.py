# карта, построение маршрута, выдача путевых и опорных точек
class Navigator:

    map = None # собственно карта
    vertexes = [] # вершины
    edges = [] # ребра

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

    # алгоритм поиска путей
    def findWays(self, startId, finishId, ways):
        return True
        #result = [x for x in self.edges if x['vertex1'] == startId or x['vertex2'] == startId]
        #if len(result):
        #    for edge in result:
        #        if edge['vertex1'] == finishId or edge['vertex2'] == finishId: # нашли конечную точку маршрута
        #            return ways.append(edge['id'])
        #        else: 
        #            ways.append(edge['id'])
        #return self.findWays(, finishId, ways)


    # найти путь полета
    def findWay(self, start, finish):

        return [x for x in self.edges if x['vertex1'] == start['id'] or x['vertex2'] == start['id']]

        #ways = []
        #self.findWays(start['id'], finish['id'], ways)
        #return ways

    # сделать полетное задание
    def makeOrder(self, options):
        start  = self.getVertex(options['start' ])
        finish = self.getVertex(options['finish'])
        if start and finish: 
            way = self.findWay(start, finish) # путь

            print(way)

            #... полет
            #... разгрузка
            #backWay = self.findWay(finish, start, self.edges) # путь обратно
            #... полет обратно
            return True
        return False
