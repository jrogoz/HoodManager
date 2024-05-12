import uuid
from typing import List
from pydantic import BaseModel, Field
from pg_connection import connect, disconnect

class NotFound(Exception):
    pass


class Sim(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str
    last_name: str
    is_alive: bool

    @classmethod
    def get_by_id(cls, sim_id: str):
        """Gets sim by id """

        conn, cur = connect()
        cur.execute("SELECT * FROM sims WHERE id={}".format(sim_id))
        record = cur.fetchone()

        if record is None:
            raise NotFound

        sim = cls(**record)  # to unpack row as dict
        disconnect(conn, cur)
        return sim

    @classmethod
    def list(cls) -> List["Sim"]:
        """Returns list of sims"""

        conn, cur = connect()
        cur.execute("SELECT * FROM sims")

        records = cur.fetchall()
        sims = [cls(**record) for record in records]
        disconnect(conn, cur)
        return sims

    def save(self) -> "Sim":
        """Insert sim into sims table"""

        conn, cur = connect()
        cur.execute(
            "INSERT INTO sims (id, first_name, last_name, is_alive) VALUES([{},{},{},{})",
            (self.id, self.first_name, self.last_name, self.is_alive)
        )
        conn.comit()
        disconnect(conn, cur)
        return self

    @classmethod
    def create_table(cls):
        conn, _ = connect()
        conn.execute(
            "CREATE TABLE IF NOT EXISTS sims (id TEXT, first_name TEXT, last_name TEXT, is_alive BOOLEAN)"
        )
        disconnect(conn)

