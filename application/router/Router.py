class Router:

    def __init__(self, app, web, mediator):
        self.web = web
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        routes = [
            ('GET', '/api/test', self.testHandler),
            ('GET', '/api/makeOrder/{type}/{priority}/{start}/{finish}', self.makeOrder), # запрос на выполнение приказа
            ('*', '/{name}', self.defaultHandler), # дефолтный хендлер
            ('*', '/', self.staticHandler) # статика
        ]
        for route in routes:
            app.router.add_route(route[0], route[1], route[2])
    
    async def testHandler(self, request):
        return self.web.json_response({ 'result': 'Hello!' })

    async def makeOrder(self, request):
        typeOrder = request.match_info.get('type') # тип маршрута (fly, delivery, landing)
        priority = request.match_info.get('priority') # приоритет маршрута (normal, high, urgent)
        start  = request.match_info.get('start') # стартовая точка маршрута
        finish = request.match_info.get('finish') # конечная точка маршрута
        if start.isdigit() and finish.isdigit():
            self.mediator.call(self.TYPES['MAKE_ORDER'], { 'start': int(start), 'finish': int(finish), 'priority': priority, 'typeOrder': typeOrder }) # послать запрос на выполнение заказа
            return self.web.json_response({ 'result': { 'start': int(start), 'finish': int(finish), 'priority': priority, 'typeOrder': typeOrder } }) # выплюнуть ответ
        return self.web.json_response({ 'error': 'order points must be numeric' })

    async def staticHandler(self, request):
        return self.web.FileResponse('./public/index.html')

    async def defaultHandler(self, request):
        return self.web.json_response({ 'result': 'no route' })
        