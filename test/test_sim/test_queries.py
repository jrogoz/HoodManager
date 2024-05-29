from residents.models import Sim
from residents.queries import ListSimsQuery, GetSimByIDQuery


def test_list_sims():
    """
    GIVEN 2 sims stored in the database
    WHEN the execute method is called
    THEN it should return 2 sims
    """
    Sim(
        first_name='Brandi',
        last_name='Broke',
        is_alive=False
    ).save()
    Sim(
        first_name='Don',
        last_name='Lothario',
        is_alive=False
    ).save()

    query = ListSimsQuery()

    assert len(query.execute()) == 2


def test_get_sim_by_id():
    """
    GIVEN ID of sim in the database
    WHEN the executed method is called on GetSimByIDQuery with an ID
    THEN id should return the sim with the same ID
    """
    sim = Sim(
        first_name='Nina',
        last_name='Caliente',
        is_alive=True
    ).save()

    query = GetSimByIDQuery(
        id=sim.id
    )

    assert query.execute().id == sim.id