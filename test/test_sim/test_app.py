import json
import pathlib

import unittest

from jsonschema import validate, RefResolver

from residents.app import app
from residents.models import Sim


def validate_payload(payload, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(
        f"{pathlib.Path(__file__).parent.absolute()}/schemas"
    )
    schema = json.loads(pathlib.Path(f"{schemas_dir}/{schema_name}").read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            "file://" + str(pathlib.Path(f"{schemas_dir}/{schema_name}").absolute()),
            schema
        )
    )


class TestAppIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Sim.create_table()

        app.config["TESTING"] = True
        cls.client = app.test_client()

    def tearDown(self):
        Sim.delete_sims()

    @classmethod
    def tearDownClass(cls):
        Sim.delete_table()

    def test_add_sim(self):
        """
        GIVEN request data for new sim
        WHEN endpoint /add-sim/ is called
        THEN it should return Sim in json format that
        """
        data = {
            'first_name': 'Alice',
            'last_name': 'Platz',
            'is_alive': bool
        }
        response = self.client.post(
            "/add-sim/",
            data=json.dumps(data),
            content_type="application/json",
        )

        validate_payload(response.json, "Sim.json")

    def test_get_sim(self):
        """
        GIVEN ID of sim stored in the database
        WHEN endpoint /sim/<id_of_sim>/ is called
        THEN it should return Sim in json format that matches the schema
        """
        sim = Sim(
            first_name='Danielle',
            last_name='Dreamer',
            is_alive=True
        ).save()
        response = self.client.get(
            f"/sim/{sim.id}",
            content_type="application/json",
        )

        validate_payload(response.json, "Sim.json")

    def test_list_sims(self):
        """
        GIVEN sims atored in the database
        WHEN endpoint /sim-list/ is called
        THEN it should return list of Sim in json format that matches the schema
        """
        Sim(
            first_name='Jane',
            last_name='Dreamer',
            is_alive=True
        ).save()
        response = self.client.get(
            "/sim-list",
            content_type="application/json",
        )

        validate_payload(response.json, "Sim.json")
