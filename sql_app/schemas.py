import datetime

from pydantic import BaseModel, ConfigDict
from .models.enums import *


class SimBase(BaseModel):
    first_name: str
    last_name: str

    hair_color: Hair
    eye_color: Eyes
    skin_tone: Skin
    race: Race | None = Race.HUMAN
    life_stage: LifeStage | None = LifeStage.BABY
    sexual_orientation: SexualOrient | None = SexualOrient.STRAIGHT

    is_alive: bool | None = True
    be_reproduced: bool | None = True


class SimCreate(SimBase):
    pass


class Sim(SimBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_update: datetime.datetime
