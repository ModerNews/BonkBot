import psycopg2
import pydantic
import datetime
from typing import Type, Union


class Bonk(pydantic.BaseModel):
    creation: datetime.datetime
    bonked: int
    bonker: int


def from_tuple(model: Type['pydantic.BaseModel'], data: Union[list, tuple]):
    temp = enumerate(model.__fields__.keys())
    return model(**{key: data[i] for i, key in temp})


class BotConnector:
    def __init__(self, host, user, password, database, use_ssh=False):
        self._use_ssh = use_ssh
        if use_ssh:
            from sshtunnel import SSHTunnelForwarder  # import here to prevent complications on import in deployment
            self.ssh_tunnel = SSHTunnelForwarder((host, 22),
                                                 ssh_username='gruzin',
                                                 ssh_password='2137',
                                                 remote_bind_address=('localhost', 5432),
                                                 local_bind_address=('localhost', 2137))
            self.ssh_tunnel.start()
        self.connection = psycopg2.connect(host=self.ssh_tunnel.local_bind_host if use_ssh else host,
                                           port=self.ssh_tunnel.local_bind_port if use_ssh else 5432,
                                           user=user,
                                           password=password,
                                           database=database)
        self.cursor = self.connection.cursor()

    def insert_new_bonk(self, bonker, bonked):
        self.cursor.execute("INSERT INTO bonking_data.last_bonks(bonker, bonked) VALUES (%s, %s)", (bonker, bonked))
        self.connection.commit()

    def get_all_bonks_by_user_bonked(self, bonked):
        self.cursor.execute("SELECT * FROM bonking_data.last_bonks WHERE bonked = %s", (bonked,))
        return [from_tuple(Bonk, record) for record in self.cursor.fetchall()]

    def delete_all_bonks_before_date(self, date: datetime.datetime):
        self.cursor.execute("DELETE FROM bonking_data.last_bonks WHERE last_bonks.creation < %s", (date,))
        self.connection.commit()

    def close(self):
        if self._use_ssh:
            self.ssh_tunnel.stop()
        self.connection.close()
        del self
