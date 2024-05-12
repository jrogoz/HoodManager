import psycopg2 as pg2
from configparser import ConfigParser


def load_config(filename='database.ini', section='postgresql') -> dict:
    """
    Return config dictionary needed for proper database connection
    :param filename: name of the file that contains config data
    :param section: name of section that contains config data
    :return: param config dictionary
    """
    parser = ConfigParser()
    try:
        parser.read(filename)
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]

        return config
    except FileNotFoundError:
        return {}


def connect(config: dict = None):
    """
    Make a database connection using given config data
    :param config: database connection params
    :return: database connection and cursor
    """

    if config is None:
        config = load_config()

    try:
        conn = pg2.connect(**config)
        cur = conn.cursor()
        return conn, cur
    except pg2.OperationalError:
        return None, None


def disconnect(conn=None, cur=None) -> None:
    """
    Close database connection
    :return: None
    """
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()