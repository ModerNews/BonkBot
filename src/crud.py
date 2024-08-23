import logging

import psycopg2
import pydantic
import datetime
from typing import Type, Union

"""
Database initalization present in 001_init.sql file
"""

LOGGER = logging.getLogger("bot.database")
RETRIES = 10

class Bonk(pydantic.BaseModel):
    creation: datetime.datetime
    bonked: int
    bonker: int


def from_tuple(model: Type['pydantic.BaseModel'], data: Union[list, tuple]):
    temp = enumerate(model.__fields__.keys())
    return model(**{key: data[i] for i, key in temp})


class BotConnector:
    def __init__(self, host, user, password, database):
        self.setup_logging()
        logging.info("Attempting initial connection to database")
        for i in range(RETRIES):
            try:
                self.connection = psycopg2.connect(host=host,
                                                   port=5432,
                                                   user=user,
                                                   password=password,
                                                   database=database)
            except psycopg2.errors.OperationalError as e:
                logging.warning(f"Failed to connect to database: {e.pgerror}; Retries left: {RETRIES - i}")
        if not self.connection.status:
            logging.error("Multiple attempts to connect to database failed, stopping")
            raise ConnectionError("Multiple attempts to connect to database failed")
        self.on_first_run()

    @staticmethod
    def setup_logging():
        handler = logging.StreamHandler()
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('\033[0;30m[{asctime}]\033[0m \033[0;34m\033[1m[{levelname:<8}]\033[0m\033[0m \033[0;35m{name}\033[0m: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)

        logger = logging.getLogger("bot.database")
        logger.addHandler(handler)


    def check_if_table_exists(self, table_name):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", (table_name,))
            return cursor.fetchone()[0]

    def init_database(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE last_bonks (
                                creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                bonked TEXT NOT NULL,
                                bonker TEXT NOT NULL);"""
                           )
            self.connection.commit()
        return True

    def on_first_run(self):
        if not self.check_if_table_exists('last_bonks'):
            logging.info("Table 'last_bonks' does not exist, creating")
            try:
                self.init_database()
            except psycopg2.Error as e:
                logging.error(f"Failed to initialize tables: {e.pgerror}, stopping")
                raise e
            return True
        logging.info("Required tables already exists, skipping initialization")

    def insert_new_bonk(self, bonker, bonked):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO last_bonks(bonker, bonked) VALUES ('%s', '%s')", (bonker, bonked))
            self.connection.commit()

    def get_all_bonks_by_user_bonked(self, bonked):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM last_bonks WHERE bonked = '%s'", (bonked,))
            return [from_tuple(Bonk, record) for record in cursor.fetchall()]

    def delete_all_bonks_before_date(self, date: datetime.datetime) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM last_bonks WHERE last_bonks.creation < %s", (date,))
            self.connection.commit()
            return cursor.rowcount

    def delete_all_bonks_by_user_bonked(self, bonked):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM last_bonks WHERE bonked = '%s'", (bonked,))
            self.connection.commit()

    def close(self):
        if self._use_ssh:
            self.ssh_tunnel.stop()
        self.connection.close()
        del self



