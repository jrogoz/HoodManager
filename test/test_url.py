import datetime

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from sql_app.main import read_sim, read_sims, create_sim
from sql_app import crud
from sql_app.schemas import SimCreate
from sql_app.models.enums import *
from sql_app.main import app, get_db


# app.dependency_overrides[get_db] = override_get_db
#
# client = TestClient(app)

def test_create_sim(client):
    sim = SimCreate(
        first_name= 'Bella',
        last_name= 'Goth',

        hair_color= Hair.BLACK,
        eye_color= Eyes.BROWN,
        skin_tone= Skin.MEDIUM,
        race= Race.HUMAN,
        life_stage= LifeStage.ADULT,
        sexual_orientation= SexualOrient.STRAIGHT,

        is_alive=False,
        be_reproduced=False
    )
    response = client.post(
        '/sims/',
        json=jsonable_encoder(sim)
    )

    assert response is not None
    assert response.status_code == 201

    sim_url = response.json()

    assert sim_url['id'] is not None
    assert isinstance(sim_url['id'], int)

    assert sim_url['last_update'] is not None
    assert isinstance(sim_url['last_update'], str)

    assert sim_url['first_name'] == sim.first_name
    assert sim_url['last_name'] == sim.last_name

    assert Hair(sim_url['hair_color']) == sim.hair_color
    assert Eyes(sim_url['eye_color']) == sim.eye_color
    assert Skin(sim_url['skin_tone']) == sim.skin_tone
    assert Race(sim_url['race']) == sim.race
    assert LifeStage(sim_url['life_stage']) == sim.life_stage
    assert SexualOrient(sim_url['sexual_orientation']) == sim.sexual_orientation

    assert sim_url['is_alive'] == sim.is_alive
    assert sim_url['be_reproduced'] == sim.be_reproduced


def test_create_sim_default_values(client):
    sim = SimCreate(
        first_name= 'Bella',
        last_name= 'Goth',

        hair_color= Hair.BLACK,
        eye_color= Eyes.BROWN,
        skin_tone= Skin.MEDIUM,
    )
    response = client.post(
        '/sims/',
        json=jsonable_encoder(sim)
    )

    assert response is not None
    assert response.status_code == 201

    sim_url = response.json()

    assert sim_url['id'] is not None
    assert isinstance(sim_url['id'], int)

    assert sim_url['last_update'] is not None
    assert isinstance(sim_url['last_update'], str)

    assert sim_url['first_name'] == sim.first_name
    assert sim_url['last_name'] == sim.last_name

    assert Hair(sim_url['hair_color']) == sim.hair_color
    assert Eyes(sim_url['eye_color']) == sim.eye_color
    assert Skin(sim_url['skin_tone']) == sim.skin_tone

    assert Race(sim_url['race']) == Race.HUMAN
    assert LifeStage(sim_url['life_stage']) == LifeStage.BABY
    assert SexualOrient(sim_url['sexual_orientation']) == SexualOrient.STRAIGHT

    assert sim_url['is_alive'] == True
    assert sim_url['be_reproduced'] == True
