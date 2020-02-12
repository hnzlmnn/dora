import logging

from playhouse.db_url import connect

from db.models import database_proxy, Entry, Line

log = logging.getLogger(__name__)


class Database:
    def __init__(self, connection, init=True):
        try:
            self.connection = connect(connection)
        except RuntimeError as e:
            # log.exception(e)
            log.error(f"Unable to parse connection string '{connection}'")
            raise
        logging.getLogger('peewee').setLevel(logging.INFO)
        if init:
            self.init()

    def init(self):
        database_proxy.initialize(self.connection)
        self.connection.create_tables([Entry, Line])

