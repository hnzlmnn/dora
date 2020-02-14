from .dora import app as dora
from .swiper import app as swiper


def add_routes(app):
    app.register_blueprint(dora, url_prefix='/dora')
    app.register_blueprint(swiper, url_prefix='/swiper')
