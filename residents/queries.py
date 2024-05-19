from typing import List
from pydantic import BaseModel

from residents.models import Sim


class ListSimsQuery(BaseModel):
    def execute(self) -> List['Sim']:
        sims = Sim.list()

        return sims


class GetSimByIDQuery(BaseModel):
    id: str

    def execute(self):
        sim = Sim.get_by_id(self.id)

        return sim