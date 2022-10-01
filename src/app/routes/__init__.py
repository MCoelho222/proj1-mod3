from flask import Flask

from src.app.controllers.users import user
from src.app.controllers.inventories import inventory
from src.app.controllers.roles import role


def routes(app: Flask):
    app.register_blueprint(user)
    app.register_blueprint(inventory)
    app.register_blueprint(role)

