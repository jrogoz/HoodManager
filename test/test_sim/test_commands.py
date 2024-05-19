import unittest

from residents.models import Sim
from residents.commands import AddSimCommand, AlreadyExists


class TestAddSimCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Sim.create_table()

    @classmethod
    def tearDownClass(cls):
        Sim.delete_table()

    def tearDown(self):
        Sim.delete_sims()

    def test_add_sim(self):
        """
        GIVEN AddSimCommand with valid first_name, last_name, and is_alive properties
        WHEN the executed method is called
        THEN a new Sim must exist in the database with the same attributes
        """
        cmd = AddSimCommand(
            first_name='Bella',
            last_name='Goth',
            is_alive=False
        )
        sim = cmd.execute()
        db_sim = Sim.get_by_id(sim.id)

        self.assertEqual(db_sim.id, sim.id)
        self.assertEqual(db_sim.first_name, sim.first_name)
        self.assertEqual(db_sim.last_name, sim.last_name)
        self.assertEqual(db_sim.is_alive, sim.is_alive)

    def test_add_sim_already_exist(self):
        """
        GIVEN AddSimCommand with a first_name and last_name equal to some Sim that already exists in database
        WHEN the execute method is called
        THEN the AlreadyExists exception must be raised
        """

        Sim(
            first_name='Bella',
            last_name='Goth',
            is_alive=False
        ).save()
        cmd = AddSimCommand(
            first_name='Bella',
            last_name='Goth',
            is_alive=True
        )

        with self.assertRaises(AlreadyExists):
            cmd.execute()
