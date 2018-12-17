class Router:

    def __init__(self, app, web, mediator):
        self.web = web
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        routes = [
            ('GET', '/api/test', self.testHandler),
            ('GET', '/api/stream', self.streamHandler),
            ('GET', '/api/pathway/make/{priority}/{start}/{finish}', self.makePathway), # запрос на создание маршрута
            ('GET', '/api/pathway/start/next'     , self.startNextPathway), # запрос на выполнение маршрута
            ('GET', '/api/pathway/start/next/{id}', self.startNextPathway), # запрос на выполнение конкретного маршрута
            ('GET', '/api/pathway/terminate', self.terminatePathway), # прекратить выполнение маршрута
            ('*', '/{name}', self.defaultHandler), # дефолтный хендлер
            ('*', '/', self.staticHandler) # статика
        ]
        for route in routes:
            app.router.add_route(route[0], route[1], route[2])

        self.mediator.subscribe(self.TYPES['CAMERA_IMAGE_CAPTURE'], self.stream)
    
    def testHandler(self, request):
        return self.web.json_response({ 'result': 'Hello!' })

    def makePathway(self, request):
        priority = request.match_info.get('priority') # приоритет маршрута (normal, high, urgent)
        start  = request.match_info.get('start') # стартовая точка маршрута
        finish = request.match_info.get('finish') # конечная точка маршрута
        if start.isdigit() and finish.isdigit():
            self.mediator.call(self.TYPES['MAKE_PATHWAY'], { 'start': int(start), 'finish': int(finish), 'priority': priority }) # послать запрос на создание маршрута
            return self.web.json_response({ 'result': { 'start': int(start), 'finish': int(finish), 'priority': priority } }) # выплюнуть ответ
        return self.web.json_response({ 'error': 'pathway points must be numeric' })

    def startNextPathway(self, request):
        id = request.match_info.get('id') # приоритет маршрута (normal, high, urgent)
        if id and id.isdigit():
            self.mediator.call(self.TYPES['START_NEXT_PATHWAY'], { 'id': int(id) }) # послать запрос на выполнение конкретного маршрута
        else:
            self.mediator.call(self.TYPES['START_NEXT_PATHWAY'], {}) # послать запрос на выполнение маршрута
        return self.web.json_response({ 'result': 'start execute pathways' })

    def terminatePathway(self, request):
        self.mediator.call(self.TYPES['TERMINATE_PATHWAY'])
        return self.web.json_response({ 'result': 'terminate pathway' })

    def stream(self, data):
        print(data)
        self.streamData = data

    def streamHandler(self, data=None):
        #print(self.streamData)
        return self.web.json_response({'result': 'ok'})

    def staticHandler(self, request):
        return self.web.FileResponse('./public/index.html')

    def defaultHandler(self, request):
        return self.web.json_response({ 'result': 'no route' })
