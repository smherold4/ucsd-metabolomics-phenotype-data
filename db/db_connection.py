from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import base
import os


def db_config():
    return "postgres://{db_username}:{db_password}@{db_host}:5432/{db_database}".format(
        db_username=os.getenv(
            'DB_USER', 'postgres'), db_password=os.getenv(
            'DB_PASSWORD', ''), db_host=os.getenv(
                'DB_HOST', '127.0.0.1'), db_database=os.getenv(
                    'DB_NAME', 'metabolomics_phenotype'))


engine = create_engine(db_config())
_SessionFactory = sessionmaker(bind=engine)


def establish(show_sql=False):
    return create_engine(db_config(), echo=show_sql)


def session_factory():
    return _SessionFactory()


def update_schema():
    engine = establish(True)
    base.Base.metadata.create_all(engine)
