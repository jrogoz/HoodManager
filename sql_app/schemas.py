import datetime

from pydantic import BaseModel, ConfigDict
from .models.enums import *


class SimBase(BaseModel):
    first_name: int
    last_name: int

    hair_color: Hair
    eye_color: Eyes
    skin_tone: Skin
    race: Race
    life_stage: LifeStage
    sexual_orientation: SexualOrient


class SimCreate(SimBase):
    pass


class Sim(SimBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_alive: bool
    be_reproduced: bool
    last_update: datetime.datetime
