import threading
import logging

from flask import Flask

from api import routes
from swiper import Swiper


log = logging.getLogger(__name__)


class ApiThread(threading.Thread):

    def __init__(self, swiper: Swiper, port: int = 3000, interface: str = '127.0.0.1'):
        threading.Thread.__init__(self)
        self.swiper = swiper
        self.interface = interface
        self.port = port
        self.setDaemon(True)

    def run(self) -> None:
        log.info(f"Starting api server on '{self.interface}:{self.port}'")
        app = Flask(__name__, static_folder=None)
        routes.add_routes(app)
        print(app.url_map)
        app.run(host=self.interface, port=self.port, debug=True, use_reloader=False)
