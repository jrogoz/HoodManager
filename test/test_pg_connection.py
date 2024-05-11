import unittest
import psycopg2 as pg2
from pg_connection import load_config, connect, disconnect


class TestLoadConfig(unittest.TestCase):

    def test_load_config_happy_path(self):
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertEqual(len(config.keys()), 5)

        expected_keys = ['host', 'database', 'user', 'password', 'port']
        for key in expected_keys:
            self.assertIn(key, config.keys())

    def test_load_config_filename_does_not_exist(self):
        config = load_config('invalid_db.ini')
        self.assertIsInstance(config, dict)
        self.assertEqual(config, {})

    def test_load_config_invalid_section(self):
        config = load_config(section='invalid_section')
        self.assertIsInstance(config, dict)
        self.assertEqual(config, {})


class TestPgConnection(unittest.TestCase):
    def setUp(self):
        self.config = load_config()

    def test_connection_happy_path(self):
        conn, cur = connect(self.config)
        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, pg2.extensions.connection)
        self.assertIsNotNone(cur)
        self.assertIsInstance(cur, pg2.extensions.cursor)
        self.assertFalse(conn.closed)

    def test_connection_invalid_db_name(self):
        self.config['database'] = 'invalid_db'
        conn, cur = connect(self.config)
        self.assertRaises(pg2.OperationalError)
        self.assertIsNone(conn)
        self.assertIsNone(cur)

    def test_connection_invalid_port_number(self):
        self.config['port'] = 5432
        conn, cur = connect(self.config)
        self.assertRaises(pg2.OperationalError)
        self.assertIsNone(conn)
        self.assertIsNone(cur)


class TestPgDisconnection(unittest.TestCase):
    def setUp(self):
        config = load_config()
        self.conn, self.cur = connect(config)

    def test_disconnect(self):
        disconnect(self.conn, self.cur)
        self.assertTrue(self.conn.closed)
        self.assertTrue(self.cur.closed)