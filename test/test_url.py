import datetime

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from sql_app import crud
from sql_app.schemas import SimCreate, SimBase
from sql_app.models.enums import *


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


def test_read_sim(client):
    response = client.post(
        '/sims/',
        json=jsonable_encoder(
            SimCreate(
                first_name= 'Bella',
                last_name= 'Goth',

                hair_color= Hair.BLACK,
                eye_color= Eyes.BROWN,
                skin_tone= Skin.MEDIUM,
    )))
    sim = response.json()
    sim_id = sim['id']

    response = client.get(f'/sims/{sim_id}')

    assert response is not None
    assert response.status_code == 200

    assert response.json() is not None
    
    readed_sim = response.json()

    assert readed_sim['id'] == sim['id']
    assert readed_sim['last_update'] == sim['last_update']

    assert readed_sim['is_alive'] == sim['is_alive']
    assert readed_sim['be_reproduced'] == sim['be_reproduced']

    assert readed_sim['first_name'] == sim['first_name']
    assert readed_sim['last_name'] == sim['last_name']

    assert readed_sim['hair_color'] == sim['hair_color']
    assert readed_sim['eye_color'] == sim['be_reproduced']
    assert readed_sim['skin_tone'] == sim['skin_tone']

    assert readed_sim['race'] == sim['race']
    assert readed_sim['life_stage'] == sim['life_stage']
    assert readed_sim['sexual_orientation'] == sim['sexual_orientation']


def test_read_sims(client):
    client.post(
        '/sims/',
        json=jsonable_encoder(
            SimCreate(
                first_name= 'Bella',
                last_name= 'Goth',

                hair_color= Hair.BLACK,
                eye_color= Eyes.BROWN,
                skin_tone= Skin.MEDIUM,
    )))
    client.post(
        '/sims/',
        json=jsonable_encoder(
            SimCreate(
                first_name= 'Mortimer',
                last_name= 'Goth',

                hair_color= Hair.BLACK,
                eye_color= Eyes.BROWN,
                skin_tone= Skin.TAN,
    )))

    response = client.get(f'/sims/')

    assert response is not None
    assert response.status_code == 200

    assert response.json() is not None

    sims = response.json()

    assert sims is not None
    assert isinstance(sims, list)
    assert len(sims) == 2


def test_update_sim(client):
    response = client.post(
        '/sims/',
        json=jsonable_encoder(
            SimCreate(
                first_name= 'Bella',
                last_name= 'Goth',

                hair_color= Hair.BLACK,
                eye_color= Eyes.BROWN,
                skin_tone= Skin.MEDIUM,
    )))
    sim_id = response.json()['id']
    create_date = response.json()['last_update']

    sim_update = SimBase(
        first_name='new name',
        last_name='new last name',

        hair_color=Hair.BLONDE,
        eye_color=Eyes.ALIEN,
        skin_tone=Skin.DARK
    )

    response = client.put(
        f'sims/{sim_id}',
        json=jsonable_encoder(sim_update)
    )

    assert response is not None
    assert response.status_code == 200

    assert response.json() is not None

    sim_db = response.json()
    
    assert sim_db['last_update'] != create_date  # not sim.last_update bc its already updated (the same memory address)
    assert sim_db['last_update'] > create_date

    assert sim_db['first_name'] == sim_update.first_name
    assert sim_db['last_name'] == sim_update.last_name

    assert Hair(sim_db['hair_color']) == sim_update.hair_color
    assert Eyes(sim_db['eye_color']) == sim_update.eye_color
    assert Skin(sim_db['skin_tone']) == sim_update.skin_tone


def test_update_sim_not_exists(client):
    sim_update = SimBase(
        first_name='new name',
        last_name='new last name',

        hair_color=Hair.BLONDE,
        eye_color=Eyes.ALIEN,
        skin_tone=Skin.DARK
    )
     
    response = client.put(
        'sims/100',
        json=jsonable_encoder(sim_update)
    )

    assert response is not None
    assert response.status_code == 404

    assert response.json() is not None
    assert response.json() == {'detail': 'Sim not found'}


def test_grow_up_sim(client):
    response = client.post(
        '/sims/',
        json=jsonable_encoder(
            SimCreate(
                first_name= 'Bella',
                last_name= 'Goth',

                hair_color= Hair.BLACK,
                eye_color= Eyes.BROWN,
                skin_tone= Skin.MEDIUM,
    )))
    sim_id = response.json()['id']
    old_life_stage = response.json()['life_stage']
    create_date = response.json()['last_update']

    response = client.put(
        f'sims/{sim_id}/grow_up',
        json={}
    )

    assert response is not None
    assert response.status_code == 200

    assert response.json() is not None

    sim_db = response.json()

    assert LifeStage(sim_db['life_stage']) == LifeStage(old_life_stage).next()
    
    assert sim_db['last_update'] != create_date
    assert sim_db['last_update'] > create_date