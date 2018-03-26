import hug

from sqlalchemy_utils.functions import database_exists, create_database, drop_database

from bankthing.db import ResourceManager
from bankthing.models import Base
import bankthing.config


@hug.get()
@hug.local()
def get_bank_data():
    """Query bank data"""
    from bankthing.tasks import fetch_bank_data
    fetch_bank_data()

    return "lol"


@hug.cli()
def create_tables(rm: ResourceManager):
    engine = rm.db.get_bind()
    db_url = engine.url
    if database_exists(db_url):
        drop_database(db_url)
    create_database(db_url)
    rm.db.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    rm.db.commit()
    Base.metadata.create_all(bind=engine)
