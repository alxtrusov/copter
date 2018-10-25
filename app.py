from aiohttp import web

from application.modules.db.DB import DB
from application.modules.userManager.UserManager import UserManager
from application.router.Router import Router

db = DB('application/modules/db/mg11.db')
userManager = UserManager(db)

print(userManager.login('vasya'))

app = web.Application()
Router(app, web)

web.run_app(app)