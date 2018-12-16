from aiohttp import web

from settings import SETTINGS
from application.modules.db.DB import DB
from application.modules.mediator.Mediator import Mediator
from application.modules.vision.Vision import Vision
from application.modules.pilot.Pilot import Pilot
from application.modules.navigator.Navigator import Navigator
from application.modules.sensor.Sensor import Sensor
from application.modules.control.Control import Control
from application.modules.user.User import User
from application.router.Router import Router

db = DB(SETTINGS['DB']) # база данных
mediator = Mediator(SETTINGS['MEDIATOR_EVENTS']) # медиатор
vision = Vision(db, mediator, SETTINGS['VISION']) # машинное видение
pilot = Pilot(db, mediator) # автопилот, управление коптером
navigator = Navigator(db, mediator, SETTINGS['MAP_ID'], SETTINGS['PATHWAY']) # карта, позиционирование, настройка карты, задание маршрутов
sensor = Sensor(db, mediator) # получение данных с датчиков расстояния
control = Control(db, mediator) # ручное управление
user = User(db, mediator) # авторизация, разграничение прав доступа

app = web.Application()
Router(app, web, mediator)

web.run_app(app)
