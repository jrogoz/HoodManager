import datetime

from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime
import enum

from .database import Base


class Hair(enum.Enum):
    BLACK: 1
    BROWN: 2
    BLONDE: 3
    RED: 4


class Eyes(enum.Enum):
    BROWN: 1
    DARK_BLUE: 2
    GREEN: 3
    LIGHT_BLUE: 4
    GREY: 5
    ALIEN: 6


class Skin(enum.Enum):
    LIGHT: 1
    TAN: 2
    MEDIUM: 3
    DARK: 4
    GREEN: 5
    WHITE: 6
    ZOMBIE: 7


class Race(enum.Enum):
    HUMAN: 1
    ALIEN: 2
    ZOMBIE: 3
    VAMPIRE: 4
    WEREWOLF: 5
    PLANTSIM: 6
    WITCH: 7


class LifeStage(enum.Enum):
    BABY: 1
    TODDLER: 2
    CHILD: 3
    TEENAGER: 4
    YOUNG_ADULT: 5
    ADULT: 6
    ELDER: 7


class SexualOrient(enum.Enum):
    NOT_SPECIFIED: 1
    STRAIGHT: 2
    GAY: 3
    BISEXUAL: 4


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
    race = Column(Enum(Race))
    life_stage = Column(Enum(LifeStage), default=LifeStage.BABY)
    sexual_orientation = Column(Enum(SexualOrient), default=SexualOrient.NOT_SPECIFIED)

    last_update = Column(DateTime, default=datetime.datetime.now())
