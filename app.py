from aiohttp import web

from settings import SETTINGS
from application.modules.db.DB import DB
from application.modules.mediator.Mediator import Mediator
from application.modules.vision.Vision import Vision
from application.modules.pilot.Pilot import Pilot
from application.modules.navigator.Navigator import Navigator
from application.modules.robot.Robot import Robot
from application.modules.control.Control import Control
from application.modules.user.User import User
from application.router.Router import Router

db = DB(SETTINGS['DB']) # база данных
mediator = Mediator(SETTINGS['MEDIATOR_EVENTS']) # медиатор
vision = Vision(db, mediator, SETTINGS['VISION']) # машинное видение
pilot = Pilot(db, mediator) # автопилот, управление коптером
navigator = Navigator(db, mediator, SETTINGS['MAP_ID'], SETTINGS['PATHWAY']) # карта, позиционирование, настройка карты, задание маршрутов
robot = Robot(db, mediator, SETTINGS['PINS']) # управление роботом
control = Control(db, mediator) # ручное управление
user = User(db, mediator) # авторизация, разграничение прав доступа


async def on_startup(app):
    print('on_startup')

async def on_cleanup(app):
    print('on_cleanup')

async def on_shutdown(app):
    print('on_shutdown')

app = web.Application()
Router(app, web, mediator)

app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)
app.on_shutdown.append(on_shutdown)

web.run_app(app)
