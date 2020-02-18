from .dora import app as dora
from .swiper import app as swiper
from .ui import app as ui


def add_routes(app):
    app.register_blueprint(dora, url_prefix='/dora')
    app.register_blueprint(swiper, url_prefix='/swiper')
    app.register_blueprint(ui, url_prefix='/')

