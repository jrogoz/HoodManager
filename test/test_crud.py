import datetime

from sql_app import crud

from sql_app.schemas import SimCreate, SimBase
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
        skin_tone=Skin.MEDIUM
    )
    sim_db = crud.create_sim(db_session, sim=sim)

    assert sim_db.is_alive is True
    assert sim_db.be_reproduced is True

    assert sim_db.race == Race.HUMAN
    assert sim_db.life_stage == LifeStage.BABY
    assert sim_db.sexual_orientation == SexualOrient.STRAIGHT


def test_get_sim(db_session):
    sim = crud.create_sim(db_session, SimCreate(
        first_name='Bella',
        last_name='Goth',

        hair_color=Hair.BLACK,
        eye_color=Eyes.BROWN,
        skin_tone=Skin.MEDIUM
    ))
    sim_db = crud.get_sim(db_session, sim_id=sim.id)

    assert sim_db is not None

    assert sim_db.id == sim.id
    assert sim_db.is_alive == sim.is_alive
    assert sim_db.be_reproduced == sim.be_reproduced
    assert sim_db.last_update == sim.last_update
    assert sim_db.race == sim.race
    assert sim_db.sexual_orientation == sim.sexual_orientation

    assert sim_db.first_name == sim.first_name
    assert sim_db.last_name == sim.last_name
    assert sim.hair_color == sim.hair_color
    assert sim.eye_color == sim.eye_color
    assert sim.skin_tone == sim.skin_tone


def test_get_sim_not_exists(db_session):
    sim_db = crud.get_sim(db_session, sim_id=1)

    assert sim_db is None


def test_get_sims(db_session):
    crud.create_sim(db_session, SimCreate(
        first_name='Bella',
        last_name='Goth',

        hair_color=Hair.BLACK,
        eye_color=Eyes.BROWN,
        skin_tone=Skin.MEDIUM
    ))
    crud.create_sim(db_session, SimCreate(
        first_name='Mortimer',
        last_name='Goth',

        hair_color=Hair.BLACK,
        eye_color=Eyes.BROWN,
        skin_tone=Skin.MEDIUM
    ))
    sims_db = crud.get_sims(db_session)

    assert sims_db is not None
    assert isinstance(sims_db, list)
    assert len(sims_db) == 2


def test_get_sims_no_sims(db_session):
    sims_db = crud.get_sims(db_session)

    assert sims_db is not None
    assert sims_db == []


def test_update_sim(db_session):
    sim = crud.create_sim(db_session, SimCreate(
        first_name='Bella',
        last_name='Goth',

        hair_color=Hair.BLACK,
        eye_color=Eyes.BROWN,
        skin_tone=Skin.MEDIUM
    ))

    create_date = sim.last_update

    sim_update = SimBase(
        first_name='new name',
        last_name='new last name',

        hair_color=Hair.BLONDE,
        eye_color=Eyes.ALIEN,
        skin_tone=Skin.DARK
    )
    sim_db = crud.update_sim(db_session, sim.id, sim_update)

    assert sim_db is not None

    assert sim_db.last_update != create_date  # not sim.last_update bc its already updated (the same memory address)
    assert sim_db.last_update > create_date

    assert sim_db.first_name == sim_update.first_name
    assert sim_db.last_name == sim_update.last_name

    assert sim_db.hair_color == sim_update.hair_color
    assert sim_db.eye_color == sim_update.eye_color
    assert sim_db.skin_tone == sim_update.skin_tone


def test_update_sim_not_exists(db_session):
    sim_update = SimBase(
        first_name='new name',
        last_name='new last name',

        hair_color=Hair.BLONDE,
        eye_color=Eyes.ALIEN,
        skin_tone=Skin.DARK
    )
    sim_db = crud.update_sim(db_session, sim_id=100, sim_update=sim_update)

    assert sim_db is None