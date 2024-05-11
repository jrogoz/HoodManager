import unittest
import psycopg2 as pg2
#from pg_connection import load_config, connect, disconnect
class TestPgConnection(unittest.TestCase):

    def test_load_config(self):
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertEqual(len(config.keys()), 5)

        expected_keys = ['host', 'databese', 'user', 'password', 'port']
        for key in expected_keys:
            self.assertIn(key, config.keys())

    def test_connection_happy_path(self):
        test_db = 'test_hm'
        user = 'postgres'
        port = 5433
        password = '12345'
        host = 'localhost'

        conn, cur = connect(db=test_db, user=user, password=password, port=port, host=host)

        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, pg2.extensions.connection)

        self.assertIsNotNone(cur)
        self.assertIsInstance(conn, pg2.extensions.cursor)

    def test_connection_invalid_db_name(self):
        test_db = 'invalid_db'
        user = 'postgres'
        port = 5433
        password = '12345'
        host = 'localhost'

        conn, cur = connect(db=test_db, user=user, password=password, port=port, host=host)
        self.assertRaises(pg2.OperationalError)
        self.assertIsNone(conn)
        self.assertIsNone(cur)

    def test_connection_invalid_port_number(self):
        test_db = 'invalid_db'
        user = 'postgres'
        port = 5432
        password = '12345'
        host = 'localhost'

        conn, cur = connect(db=test_db, user=user, password=password, port=port, host=host)
        self.assertRaises(pg2.OperationalError)
        self.assertIsNone(conn)
        self.assertIsNone(cur)


conn = pg2.connect(database='dvdrental', user='postgres', password='12345',port=5432)
cur = conn.cursor()
print(type(cur))
print(pg2.extensions.connection)

print(type(cur) is pg2.extensions.cursor)


print(type({}))