import os
import tempfile

import pytest

from residents.models import Sim


@pytest.fixture(autouse=True)
def database():
    Sim.create_table()
    yield
    Sim.delete_table()

