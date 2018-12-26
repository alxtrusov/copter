import base64
import time

class Router:

    def __init__(self, app, web, mediator):
        self.web = web
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        self.vecArr, self.streamData = ([], [])
        routes = [
            ('GET', '/api/test', self.testHandler),
            ('GET', '/api/stream', self.streamHandler),
            ('GET', '/api/pathway/make/{priority}/{start}/{finish}', self.makePathway), # запрос на создание маршрута
            ('GET', '/api/pathway/start/next'     , self.startNextPathway), # запрос на выполнение маршрута
            ('GET', '/api/pathway/start/next/{id}', self.startNextPathway), # запрос на выполнение конкретного маршрута
            ('GET', '/api/pathway/terminate', self.terminatePathway), # прекратить выполнение маршрута
            ('GET', '/api/shutdown', self.shutdown), # выключить малину
            ('GET', '/api/reboot', self.reboot), # ребутнуть малину
            ('GET', '/api/present/drop', self.dropPresent), # скинуть подарки
            #('*', '/{name}', self.defaultHandler), # дефолтный хендлер
            ('*', '/', self.staticHandler) # статика
        ]
        app.router.add_static('/js/', path=str('./public/js/'))
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

    def shutdown(self, request):
        self.mediator.call(self.TYPES['SHUTDOWN'])
        return self.web.json_response({ 'result': 'shutdown' })

    def reboot(self, request):
        self.mediator.call(self.TYPES['REBOOT'])
        return self.web.json_response({ 'result': 'reboot' })

    def dropPresent(self, request):
        self.mediator.call(self.TYPES['FIRE_DROP_PRESENT'])
        return self.web.json_response({ 'result': 'presents dropped' })

    def stream(self, data):
        self.vecArr, self.streamData = data

    def streamHandler(self, data=None):
        image = self.streamData
        data = base64.b64encode(bytearray(image))
        return self.web.json_response({'result': data.decode('utf-8')})

    def staticHandler(self, request):
        return self.web.FileResponse('./public/index.html')

    def defaultHandler(self, request):
        return self.web.json_response({ 'result': 'no route' })
