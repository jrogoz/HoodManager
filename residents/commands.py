from pydantic import BaseModel
from residents.models import Sim, NotFound


class AlreadyExists(Exception):
    pass


class AddSimCommand(BaseModel):
    first_name: str
    last_name: str
    is_alive: bool

    def execute(self) -> Sim:
        try:
            Sim.get_by_name(self.first_name, self.last_name)
            raise AlreadyExists
        except NotFound:
            pass

        sim = Sim(
            first_name=self.first_name,
            last_name=self.last_name,
            is_alive=self.is_alive

        ).save()

        return sim
