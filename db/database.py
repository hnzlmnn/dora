import logging

from playhouse.db_url import connect

from db.models import database_proxy, Entry, Line, Meta

log = logging.getLogger(__name__)


class Database:
    __INSTANCE = None

    def __init__(self, connection, init=True):
        try:
            self.connection = connect(connection)
        except RuntimeError as e:
            # log.exception(e)
            log.error(f"Unable to parse connection string '{connection}'")
            raise
        logging.getLogger('peewee').setLevel(logging.DEBUG)
        if init:
            self.init()

    @staticmethod
    def instance(*args, **kwargs):
        if Database.__INSTANCE is None:
            Database.__INSTANCE = Database(*args, **kwargs)
        return Database.__INSTANCE

    def init(self):
        database_proxy.initialize(self.connection)
        self.connection.create_tables([Entry, Line, Meta])

    def connect(self):
        self.connection.connect(True)

    def close(self):
        self.connection.close()

