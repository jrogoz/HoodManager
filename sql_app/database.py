from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345@db/HoodManagerDB'

URL_OBJECT = URL.create(
    'postgresql',
    username='postgres',
    password='12345',
    host='localhost',
    database='HoodManagerDB',
    port=5432
)

engine = create_engine(URL_OBJECT)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()