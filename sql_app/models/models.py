import datetime

from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime

from sql_app.database import Base
from enums import *


class Sim(Base):
    __tablename__ = 'sims'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    is_alive = Column(Boolean, default=True)
    be_reproduced = Column(Boolean, default=True)

    hair_color = Column(Enum(Hair))
    eye_color = Column(Enum(Eyes))
    skin_tone = Column(Enum(Skin))
    race = Column(Enum(Race), default=Race.HUMAN)
    life_stage = Column(Enum(LifeStage), default=LifeStage.BABY)
    sexual_orientation = Column(Enum(SexualOrient), default=SexualOrient.NOT_SPECIFIED)

    last_update = Column(DateTime, default=datetime.datetime.now())
