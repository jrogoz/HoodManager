import datetime

from sql_app import crud

from sql_app.schemas import SimCreate
from sql_app.models.enums import *


def test_create_sim(db_session):
    sim = SimCreate(
        first_name='Bella',
        last_name='Goth',

        hair_color=Hair.BLACK,
        eye_color=Eyes.BROWN,
        skin_tone=Skin.MEDIUM,
        race=Race.HUMAN,
        life_stage=LifeStage.ADULT,
        sexual_orientation=SexualOrient.STRAIGHT,

        is_alive=False,
        be_reproduced=False
    )
    sim_db = crud.create_sim(db_session, sim=sim)

    assert sim_db is not None
    assert sim_db.id is not None
    assert isinstance(sim_db.id, int)

    assert sim_db.last_update is not None
    assert isinstance(sim_db.last_update, datetime.date)

    assert sim_db.first_name == sim.first_name
    assert sim_db.last_name == sim.last_name

    assert sim_db.hair_color == sim.hair_color
    assert sim_db.eye_color == sim.eye_color
    assert sim_db.skin_tone == sim.skin_tone
    assert sim_db.race == sim.race
    assert sim_db.life_stage == sim.life_stage
    assert sim_db.sexual_orientation == sim.sexual_orientation

    assert sim_db.is_alive == sim.is_alive
    assert sim_db.be_reproduced == sim.be_reproduced


def test_create_sim_default_values(db_session):
    sim = SimCreate(
        first_name='Bella',
        last_name='Goth',

        hair_color=Hair.BLACK,
        eye_color=Eyes.BROWN,
        skin_tone=Skin.MEDIUM,
    )
    sim_db = crud.create_sim(db_session, sim=sim)

    assert sim_db.is_alive is True
    assert sim_db.be_reproduced is True

    assert sim_db.race == Race.HUMAN
    assert sim_db.life_stage == LifeStage.BABY
    assert sim_db.sexual_orientation == SexualOrient.STRAIGHT
