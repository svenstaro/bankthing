import hug
import os

from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


def make_session():
    import bankthing.config
    engine = create_engine(os.environ['DATABASE_URI'], echo=True)
    session_factory = scoped_session(sessionmaker(bind=engine))
    return session_factory()


@hug.directive()
class ResourceManager(object):
    def __init__(self, *args, **kwargs):
        self._db = make_session()
        self.autocommit = False

    @property
    def db(self) -> Session:
        return self._db

    def cleanup(self, exception=None):
        if exception:
            # self.db.remove()
            self.db.rollback()
            return
        if self.autocommit:
            self.db.commit()
        # self.db.remove()


# @hug.directive()
# def return_session() -> Session:
#     return session_factory()
